"""
graph/router.py — Query Router

Decides whether a user query should go to the RAG Agent or the MCP Agent.

Routing strategy (keyword-based):
  Simple and transparent — no LLM call needed for routing.
  We scan the query for keywords that signal tool use (math, weather).
  Everything else defaults to RAG (document Q&A).

  Why not use an LLM to route?
    - Adds latency and cost for a decision that keyword matching handles well
    - Keywords are deterministic — easier to debug and extend
    - You can always upgrade to LLM-based routing later

Route values:
  "mcp" → send to MCP Tool Agent (calculator, weather)
  "rag" → send to RAG Agent (document retrieval)
"""

from config import MCP_TRIGGER_KEYWORDS


def decide_route(query: str) -> str:
    """
    Inspect `query` and return the agent route.

    Parameters
    ----------
    query : str
        The user's raw question.

    Returns
    -------
    str
        "mcp" if any MCP trigger keyword is found (case-insensitive),
        "rag" otherwise.
    """
    query_lower = query.lower()

    for keyword in MCP_TRIGGER_KEYWORDS:
        if keyword in query_lower:
            print(f"  🔀 Router → MCP  (matched keyword: '{keyword}')")
            return "mcp"

    print("  🔀 Router → RAG  (no tool keywords found)")
    return "rag"
