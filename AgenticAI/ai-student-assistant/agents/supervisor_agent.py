"""
agents/supervisor_agent.py
──────────────────────────
The Supervisor Agent: the "traffic controller" of the multi-agent system.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT DOES THE SUPERVISOR DO?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
After every agent runs, control returns to the Supervisor.
The Supervisor looks at the current state and decides:
  "Is there more work to do?  If so, which agent should go next?"

Think of it like a project manager:
  • Reads the current status (what's been done).
  • Assigns the next task to the right person.
  • Recognises when the project is complete.

DECISION TREE
─────────────
  Already have final_answer?
    └─► END

  Nothing gathered yet?
    ├─► Query needs documents?    → rag_agent
    └─► Query needs calculation?  → mcp_agent
        Otherwise                 → answer_agent (general knowledge)

  Have RAG context but no answer yet?
    └─► answer_agent

  Have tool results but no answer yet?
    └─► answer_agent

  Safety: iteration_count >= MAX_ITERATIONS?
    └─► answer_agent  (force finish)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHY USE AN LLM FOR ROUTING?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Simple rule-based routing ("if 'calculate' in query → mcp_agent") breaks
for natural language ("what's 15% tip on $47.50?").

By asking Claude to read the state and decide, we get routing that
understands natural language intent.  We use the FAST (Haiku) model here
to keep routing cheap and quick.
"""

from langchain_core.output_parsers import StrOutputParser

from agents.base_agent import BaseAgent
from chains.prompts import SUPERVISOR_PROMPT
from graph.state import AgentState
from config import settings
from utils.llm_factory import get_fast_llm
from utils.logger import get_logger

log = get_logger(__name__)

# Valid routing targets – anything else is a bug
_VALID_TARGETS = {"rag_agent", "mcp_agent", "answer_agent", "END"}

# Fast chain for routing
_routing_chain = SUPERVISOR_PROMPT | get_fast_llm() | StrOutputParser()


class SupervisorAgent(BaseAgent):
    """
    Reads the current AgentState and decides which agent runs next.

    Only sets state["next_agent"] and increments state["iteration_count"].
    Does NOT generate any answer content.
    """

    def __init__(self) -> None:
        super().__init__("SupervisorAgent")

    def _execute(self, state: AgentState) -> AgentState:
        iteration = state.get("iteration_count", 0) + 1

        # ── Safety: force finish if we've looped too many times ───────────────
        if iteration > settings.max_iterations:
            log.warning("Max iterations (%d) reached – forcing answer_agent",
                        settings.max_iterations)
            return {                                         # type: ignore
                "next_agent": "answer_agent",
                "iteration_count": iteration,
            }

        # ── Already done? ─────────────────────────────────────────────────────
        if state.get("final_answer"):
            log.info("Final answer already written → END")
            return {"next_agent": "END", "iteration_count": iteration}  # type: ignore

        # ── Agent error detected? Skip to answer_agent ────────────────────────
        if state.get("error"):
            log.warning("Error in state: %s → forcing answer_agent", state["error"][:80])
            return {"next_agent": "answer_agent", "iteration_count": iteration, "error": ""}  # type: ignore

        # ── Ask the LLM to decide ─────────────────────────────────────────────
        decision = _routing_chain.invoke({
            "query":          state["query"],
            "has_rag":        bool(state.get("rag_context")),
            "has_tools":      bool(state.get("tool_results")),
            "has_answer":     bool(state.get("final_answer")),
            "iteration":      iteration,
            "max_iterations": settings.max_iterations,
        })

        # Clean up the decision (LLMs sometimes add punctuation or spaces)
        next_agent = decision.strip().lower().rstrip(".")

        # Validate: if the LLM returns something unexpected, default to answer
        if next_agent not in _VALID_TARGETS:
            log.warning("Unexpected routing decision: %r → defaulting to answer_agent",
                        next_agent)
            next_agent = "answer_agent"

        log.info("Routing → [bold yellow]%s[/bold yellow]  (iteration %d)",
                 next_agent, iteration)

        return {                                             # type: ignore
            "next_agent": next_agent,
            "iteration_count": iteration,
            "history": [{
                "role": "system",
                "content": f"Supervisor[iter={iteration}] → {next_agent}",
            }],
        }


# ── Singleton ─────────────────────────────────────────────────────────────────
supervisor_agent = SupervisorAgent()
