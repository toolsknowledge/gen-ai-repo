"""
agents/answer_agent.py
──────────────────────
The Answer Agent: synthesises a final answer from all gathered context.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHERE DOES THIS AGENT FIT?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The Answer Agent is always the LAST agent to run before the graph returns
to the user.  By this point:

  state["rag_context"]   is filled (if RAG Agent ran)
  state["tool_results"]  is filled (if MCP Tool Agent ran)
  state["history"]       contains a log of everything that happened

This agent:
  1. Reads all that context.
  2. Calls generate_answer() from chains/answer_chain.py (an LCEL chain).
  3. Writes the polished answer to state["final_answer"].
  4. Sets state["next_agent"] = "END" to signal the graph to stop.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DESIGN NOTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This agent is intentionally thin.  All the heavy lifting (prompt templates,
LLM calls, output parsing) lives in chains/answer_chain.py.
This separation makes it easy to test the chain without spinning up the
full graph.
"""

from agents.base_agent import BaseAgent
from chains.answer_chain import generate_answer
from graph.state import AgentState
from utils.logger import get_logger

log = get_logger(__name__)


class AnswerAgent(BaseAgent):
    """
    Synthesises the final answer from RAG context and tool results.

    Inputs (from state):
      • query         – the user's question
      • rag_context   – retrieved document chunks
      • tool_results  – MCP tool call results

    Outputs (to state):
      • final_answer  – the complete, formatted answer string
      • next_agent    – set to "END" to stop the graph
    """

    def __init__(self) -> None:
        super().__init__("AnswerAgent")

    def _execute(self, state: AgentState) -> AgentState:
        query        = state["query"]
        rag_context  = state.get("rag_context", "")
        tool_results = state.get("tool_results", {})

        log.info(
            "Generating final answer (rag=%d chars, tools=%s)",
            len(rag_context),
            list(tool_results.keys()) if tool_results else "none",
        )

        # Delegate to the LCEL chain
        answer = generate_answer(
            query=query,
            rag_context=rag_context,
            tool_results=tool_results,
        )

        log.info("Answer generated (%d chars)", len(answer))

        return {                                             # type: ignore
            "final_answer": answer,
            "next_agent": "END",        # tell the router to stop
            "history": [{
                "role": "assistant",
                "content": answer,
            }],
        }


# ── Singleton ─────────────────────────────────────────────────────────────────
answer_agent = AnswerAgent()
