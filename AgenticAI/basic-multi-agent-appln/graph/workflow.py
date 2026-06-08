"""
graph/workflow.py — LangGraph Workflow Compiler

Assembles nodes and edges into a compiled, runnable graph.

Graph topology
--------------

  [START]
     │
     ▼
 router_node          ← always runs first
     │
     ├─── route=="rag" ──► rag_node ──► [END]
     │
     └─── route=="mcp" ──► mcp_node ──► [END]
                                │
                         (error) ──► error_node ──► [END]

Usage
-----
from graph.workflow import build_graph

graph = build_graph()
result = graph.invoke({"query": "What is LangGraph?"})
print(result["final_response"])
"""

from langgraph.graph import StateGraph, END

from graph.state import AgentState
from graph.nodes import (
    router_node,
    rag_node,
    mcp_node,
    error_node,
    route_decision,
)


def build_graph() -> StateGraph:
    """
    Build and compile the LangGraph workflow.

    Steps
    -----
    1. Create a StateGraph typed with AgentState
    2. Add nodes (processing steps)
    3. Set the entry point
    4. Add a conditional edge from router → rag or mcp
    5. Add terminal edges from rag/mcp/error → END
    6. Compile and return

    Returns
    -------
    CompiledGraph
        A runnable graph. Call graph.invoke({"query": "..."}) to run it.
    """

    # ── 1. Create graph ───────────────────────────────────────────────────────
    graph = StateGraph(AgentState)

    # ── 2. Register nodes ─────────────────────────────────────────────────────
    graph.add_node("router_node", router_node)
    graph.add_node("rag_node",    rag_node)
    graph.add_node("mcp_node",    mcp_node)
    graph.add_node("error_node",  error_node)

    # ── 3. Entry point ────────────────────────────────────────────────────────
    graph.set_entry_point("router_node")

    # ── 4. Conditional edge: router → rag | mcp | error ──────────────────────
    graph.add_conditional_edges(
        "router_node",          # source node
        route_decision,         # function that returns next-node name
        {                       # mapping: return-value → node name
            "rag_node":   "rag_node",
            "mcp_node":   "mcp_node",
            "error_node": "error_node",
        },
    )

    # ── 5. Terminal edges ─────────────────────────────────────────────────────
    graph.add_edge("rag_node",   END)
    graph.add_edge("mcp_node",   END)
    graph.add_edge("error_node", END)

    # ── 6. Compile ────────────────────────────────────────────────────────────
    compiled = graph.compile()

    print("  ✅ LangGraph workflow compiled successfully.")
    return compiled


# ── Module-level singleton ────────────────────────────────────────────────────
# Import this in other modules to avoid recompiling the graph on every call.

_graph = None


def get_graph():
    """Return (or lazily create) the compiled graph singleton."""
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph
