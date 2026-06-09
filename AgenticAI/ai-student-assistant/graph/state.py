"""
graph/state.py
──────────────
Defines AgentState – the single shared data structure that flows through
every node in the LangGraph graph.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IS STATE?  (Beginner explanation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Imagine a sheet of paper that gets passed from agent to agent.
  1. User writes a question on it.
  2. Supervisor reads it, writes "go to RAG Agent".
  3. RAG Agent retrieves context, writes the chunks on the paper.
  4. Supervisor reads again, writes "go to Answer Agent".
  5. Answer Agent reads everything, writes the final answer.
  6. Graph returns the paper to the user.

AgentState IS that "sheet of paper".

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHY TypedDict instead of a dataclass?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LangGraph requires state to be a TypedDict (or a Pydantic model).
TypedDict is just a plain Python dict with type annotations – no overhead,
easy to serialize, and LangGraph knows how to merge partial updates from
different nodes using Annotated[list, operator.add] (append semantics).
"""

import operator
from typing import Annotated, Any
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """
    The single shared state object passed between every LangGraph node.

    Field-by-field explanation
    ──────────────────────────
    query          : The raw question the user asked.  Set once, never changed.

    history        : Running list of {"role": ..., "content": ...} messages,
                     appended by each agent.  Gives the Answer Agent full
                     conversation context.
                     Annotated[list, operator.add] tells LangGraph to APPEND
                     items rather than replace the whole list.

    rag_context    : Text chunks retrieved from ChromaDB.  Set by RAG Agent.

    tool_results   : Dict of {tool_name: result_string} set by MCP Tool Agent.

    final_answer   : The polished answer written by Answer Agent.

    next_agent     : Which node to visit next.  The Supervisor writes this;
                     the conditional edge reads it to route the graph.
                     Values: "rag_agent" | "mcp_agent" | "answer_agent" | "END"

    iteration_count: Safety counter.  If the Supervisor loops > MAX_ITERATIONS
                     we force-stop to avoid infinite loops.

    error          : Optional error message from any agent.
    """

    # ── Inputs ────────────────────────────────────────────────────────────────
    query: str

    # ── Accumulated data (append-only lists) ──────────────────────────────────
    # operator.add means: new_value = old_list + new_list  (not replacement)
    history: Annotated[list[dict[str, Any]], operator.add]

    # ── Agent outputs ─────────────────────────────────────────────────────────
    rag_context: str           # filled by RAG Agent
    tool_results: dict         # filled by MCP Tool Agent
    final_answer: str          # filled by Answer Agent

    # ── Routing ───────────────────────────────────────────────────────────────
    next_agent: str            # written by Supervisor, read by router edge
    iteration_count: int       # incremented by Supervisor each loop

    # ── Diagnostics ───────────────────────────────────────────────────────────
    error: str                 # set if any agent raises an exception


def create_initial_state(query: str) -> AgentState:
    """
    Build the initial AgentState for a new user question.

    Called by main.py / tests before invoking the graph.
    All fields have sensible defaults so agents can safely read them without
    KeyError even on the first pass.
    """
    return AgentState(
        query=query,
        history=[{"role": "user", "content": query}],
        rag_context="",
        tool_results={},
        final_answer="",
        next_agent="supervisor",  # always start with the Supervisor
        iteration_count=0,
        error="",
    )
