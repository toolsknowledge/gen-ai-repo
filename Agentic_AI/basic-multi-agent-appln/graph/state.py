"""
graph/state.py — LangGraph Shared State

AgentState is the single dict that flows through every node in the graph.
Each node reads fields it needs and writes fields it produces.

Think of it like a baton in a relay race — every runner (node) can
read what previous runners wrote, and adds their own contribution.

Fields
------
query          : the original user question (set once, never changed)
route          : "rag" or "mcp" — set by the router node
context        : retrieved document chunks (RAG only)
tool_result    : raw output from MCP tool calls (MCP only)
final_response : the finished answer from Claude (last node writes this)
error          : any error message; non-None signals something went wrong
"""

from typing import Optional
from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    """
    Shared state passed between all LangGraph nodes.

    All fields are optional (total=False) so each node only needs to
    declare the fields it touches — not fill in every key.
    """

    # ── Input ────────────────────────────────────────────────────────────────
    query: str                    # The user's original question

    # ── Routing ─────────────────────────────────────────────────────────────
    route: str                    # "rag" | "mcp"

    # ── RAG Agent outputs ────────────────────────────────────────────────────
    context: str                  # Retrieved document chunks (joined text)
    source_docs: list             # Raw Document objects (for citations)

    # ── MCP Agent outputs ────────────────────────────────────────────────────
    tool_result: str              # Formatted tool output from MCP server

    # ── Final output ─────────────────────────────────────────────────────────
    final_response: str           # Claude's final answer to the user

    # ── Error handling ───────────────────────────────────────────────────────
    error: Optional[str]          # None = all good; str = something failed
