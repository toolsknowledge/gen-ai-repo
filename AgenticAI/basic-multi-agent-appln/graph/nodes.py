"""
graph/nodes.py — LangGraph Node Functions

Each function here is one node in the LangGraph graph.
A node receives the current AgentState, does its work,
and returns a dict of fields to merge back into the state.

Nodes defined here
------------------
router_node   : sets state["route"] using the keyword router
rag_node      : retrieves context from ChromaDB, calls Claude
mcp_node      : calls MCP tools, passes results to Claude
error_node    : formats a graceful error response
"""

from graph.state import AgentState
from graph.router import decide_route
from agents.rag_agent import run_rag_agent
from agents.mcp_agent import run_mcp_agent


# ── Router Node ──────────────────────────────────────────────────────────────

def router_node(state: AgentState) -> AgentState:
    """
    Inspect the query and write the routing decision into state.

    This node runs FIRST in the graph. Its only job is to set
    state["route"] so the conditional edge knows where to send next.
    """
    query = state.get("query", "")
    route = decide_route(query)
    return {"route": route}


# ── RAG Node ─────────────────────────────────────────────────────────────────

def rag_node(state: AgentState) -> AgentState:
    """
    Run the RAG pipeline:
      1. Retrieve relevant document chunks from ChromaDB
      2. Build a prompt with retrieved context
      3. Call Claude for a grounded answer
      4. Write final_response (and context) back to state

    Called only when route == "rag".
    """
    query = state.get("query", "")

    try:
        result = run_rag_agent(query)
        return {
            "context": result["context"],
            "source_docs": result["source_docs"],
            "final_response": result["response"],
            "error": None,
        }
    except Exception as exc:
        return {
            "final_response": f"RAG Agent error: {exc}",
            "error": str(exc),
        }


# ── MCP Node ──────────────────────────────────────────────────────────────────

def mcp_node(state: AgentState) -> AgentState:
    """
    Run the MCP Tool pipeline:
      1. Send query to MCP agent, which calls the right tool
      2. Pass tool output back to Claude for a natural-language response
      3. Write final_response (and tool_result) back to state

    Called only when route == "mcp".
    """
    query = state.get("query", "")

    try:
        result = run_mcp_agent(query)
        return {
            "tool_result": result["tool_result"],
            "final_response": result["response"],
            "error": None,
        }
    except Exception as exc:
        return {
            "final_response": f"MCP Agent error: {exc}",
            "error": str(exc),
        }


# ── Error Node ────────────────────────────────────────────────────────────────

def error_node(state: AgentState) -> AgentState:
    """
    Catch-all fallback node. Produces a user-friendly error message
    when something goes wrong earlier in the graph.
    """
    error = state.get("error", "An unknown error occurred.")
    return {
        "final_response": (
            f"⚠️ Something went wrong: {error}\n\n"
            "Please check your configuration and try again."
        )
    }


# ── Conditional edge function ─────────────────────────────────────────────────

def route_decision(state: AgentState) -> str:
    """
    Used by LangGraph's add_conditional_edges().
    Maps state["route"] to the next node name.

    Returns
    -------
    str  — one of: "rag_node", "mcp_node", "error_node"
    """
    if state.get("error"):
        return "error_node"

    route = state.get("route", "rag")
    if route == "mcp":
        return "mcp_node"
    return "rag_node"
