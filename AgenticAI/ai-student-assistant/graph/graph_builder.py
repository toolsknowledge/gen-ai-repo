"""
graph/graph_builder.py
──────────────────────
Assembles the LangGraph StateGraph that orchestrates all four agents.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IS LANGGRAPH?  (Beginner explanation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LangGraph is a library for building stateful, multi-step AI applications
as a directed graph.

Core concepts:
  • Node   – a Python function (or agent) that transforms the state.
  • Edge   – a connection from one node to another.
  • Conditional Edge – a router that picks the next node dynamically
                       based on the current state.
  • State  – the shared TypedDict that flows between nodes.

GRAPH TOPOLOGY
──────────────
  START
    │
    ▼
  [supervisor]  ←────────────────────────────────┐
    │                                             │
    │  (conditional edge reads state.next_agent) │
    ├─── "rag_agent"   → [rag_agent]   ──────────┤
    ├─── "mcp_agent"   → [mcp_agent]   ──────────┤
    ├─── "answer_agent"→ [answer_agent]──────────┤
    └─── "END"         → END                      │
                         ↑                        │
                         │ [answer_agent] always  │
                         │ goes back to supervisor│
                         └────────────────────────┘

Wait, answer_agent sets next_agent="END", so supervisor routes to END
on the next call.  The graph terminates after answer_agent → supervisor → END.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOW DOES THE CONDITIONAL EDGE WORK?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_conditional_edges(
    "supervisor",         # FROM this node
    router_fn,            # call this function to decide which node to go to
    {                     # mapping: return value → node name
        "rag_agent":    "rag_agent",
        "mcp_agent":    "mcp_agent",
        "answer_agent": "answer_agent",
        "END":          END,
    }
)

After [supervisor] runs, LangGraph calls router_fn(state).
router_fn reads state["next_agent"] and returns the string name of the
next node.  LangGraph looks it up in the mapping and jumps to that node.
"""

from langgraph.graph import StateGraph, END

from graph.state import AgentState
from agents.supervisor_agent import supervisor_agent
from agents.rag_agent import rag_agent
from agents.mcp_tool_agent import mcp_tool_agent
from agents.answer_agent import answer_agent
from utils.logger import get_logger

log = get_logger(__name__)


# ── Router function ────────────────────────────────────────────────────────────
_VALID_ROUTES = {"rag_agent", "mcp_agent", "answer_agent", "END"}

def route_to_next_agent(state: AgentState) -> str:
    """
    Reads state["next_agent"] and returns the name of the next node.

    Falls back to "END" for any unknown value (e.g. "supervisor" left over
    from the initial state when an agent errors before writing next_agent).
    """
    next_node = state.get("next_agent", "END")
    if next_node not in _VALID_ROUTES:
        log.warning("Router: unknown next_agent=%r → defaulting to END", next_node)
        return "END"
    log.debug("Router: next_agent=%s", next_node)
    return next_node


# ── Build the graph ────────────────────────────────────────────────────────────
def build_graph():
    """
    Construct and compile the LangGraph StateGraph.

    Returns a compiled graph object that can be invoked with:
        graph.invoke(initial_state)
    """
    # 1. Create the graph with our AgentState type
    graph = StateGraph(AgentState)

    # 2. Add nodes – each node is an agent's .run() method
    #    Node name (string) must match the routing targets in supervisor_agent.py
    graph.add_node("supervisor",   supervisor_agent.run)
    graph.add_node("rag_agent",    rag_agent.run)
    graph.add_node("mcp_agent",    mcp_tool_agent.run)
    graph.add_node("answer_agent", answer_agent.run)

    # 3. Set entry point – the first node to run
    graph.set_entry_point("supervisor")

    # 4. Add the conditional edge from supervisor
    #    After supervisor runs, call route_to_next_agent(state) to decide where to go
    graph.add_conditional_edges(
        "supervisor",
        route_to_next_agent,
        {
            "rag_agent":    "rag_agent",
            "mcp_agent":    "mcp_agent",
            "answer_agent": "answer_agent",
            "END":          END,           # LangGraph built-in terminal node
        },
    )

    # 5. All worker agents loop back to the supervisor
    #    This is what creates the "re-plan after each step" behaviour.
    graph.add_edge("rag_agent",    "supervisor")
    graph.add_edge("mcp_agent",    "supervisor")
    graph.add_edge("answer_agent", "supervisor")

    # 6. Compile – validates the graph structure and returns an executable object
    compiled = graph.compile()
    log.info("Graph compiled successfully ✓")

    return compiled


# ── Singleton ─────────────────────────────────────────────────────────────────
student_assistant_graph = build_graph()
