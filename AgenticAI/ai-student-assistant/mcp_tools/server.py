"""
mcp_tools/server.py
───────────────────
The MCP (Model Context Protocol) server that exposes tools the agent can call.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IS MCP?  (Beginner explanation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MCP (Model Context Protocol) is an open standard created by Anthropic that
defines a universal interface for LLMs to call external tools.

Without MCP: each application writes its own ad-hoc tool wrappers.
With MCP:    any MCP-compatible client (Claude, VS Code, etc.) can
             automatically discover and call any MCP-compatible server.

Think of MCP like USB:
  • USB defines a standard connector.
  • Any device that follows the USB spec works with any USB port.
  • MCP defines a standard message format (JSON-RPC over stdio/HTTP).
  • Any MCP server's tools are automatically available to MCP clients.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOW THIS SERVER WORKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. We create an MCP Server object and register tool functions with @server.tool()
  2. The MCP Tool Agent spawns this server as a subprocess (stdio transport).
  3. The agent sends a JSON-RPC request: {"method": "tools/call", "params": {...}}
  4. The server executes the Python function and returns a JSON-RPC response.
  5. The agent reads the response and writes it to state["tool_results"].

TOOLS IMPLEMENTED
─────────────────
  • calculate        : evaluate a mathematical expression (e.g. "2 + 2 * 10")
  • get_current_date : return today's date and time
  • web_search       : stub that returns a placeholder (replace with real API)

RUN THIS SERVER STANDALONE (for testing):
  python mcp_tools/server.py
"""

import ast
import math
import operator
import datetime
from mcp.server.fastmcp import FastMCP

# ── Create the MCP Server ─────────────────────────────────────────────────────
# FastMCP is a convenience wrapper around the base MCP Server that reduces
# boilerplate.  The name "student-assistant" is what clients see when they
# list available servers.
mcp = FastMCP("student-assistant")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 1 – Safe Calculator
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# A whitelist of safe operations for the expression evaluator.
# NEVER use eval() on user input – it can execute arbitrary code.
_SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}
_SAFE_NAMES = {
    "abs": abs, "round": round,
    "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "pi": math.pi, "e": math.e,
}


def _safe_eval(expr: str) -> float:
    """Evaluate a math expression safely without eval()."""
    def _eval_node(node):
        if isinstance(node, ast.Constant):               # numbers
            return node.value
        if isinstance(node, ast.BinOp):                  # a + b
            op = _SAFE_OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operator: {type(node.op)}")
            return op(_eval_node(node.left), _eval_node(node.right))
        if isinstance(node, ast.UnaryOp):                # -x
            op = _SAFE_OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported unary operator")
            return op(_eval_node(node.operand))
        if isinstance(node, ast.Call):                   # sqrt(4)
            func_name = node.func.id if isinstance(node.func, ast.Name) else None
            func = _SAFE_NAMES.get(func_name)
            if func is None:
                raise ValueError(f"Unknown function: {func_name}")
            args = [_eval_node(a) for a in node.args]
            return func(*args)
        if isinstance(node, ast.Name):                   # pi, e
            val = _SAFE_NAMES.get(node.id)
            if val is None:
                raise ValueError(f"Unknown name: {node.id}")
            return val
        raise ValueError(f"Unsupported expression type: {type(node)}")

    tree = ast.parse(expr, mode="eval")
    return _eval_node(tree.body)


@mcp.tool()
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression and return the result.

    Examples
    --------
    calculate("2 + 2")              → "4.0"
    calculate("sqrt(144)")          → "12.0"
    calculate("(10 + 5) * 3 / 4")  → "11.25"
    calculate("2 ** 10")            → "1024.0"

    Parameters
    ----------
    expression : A mathematical expression as a string.
                 Supports: +, -, *, /, ** (power), sqrt, sin, cos, tan,
                           log, log10, abs, round, pi, e
    """
    try:
        result = _safe_eval(expression.strip())
        # Format integers nicely (no trailing .0)
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(round(result, 8))
    except Exception as exc:
        return f"Error evaluating '{expression}': {exc}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 2 – Date / Time
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@mcp.tool()
def get_current_date(timezone: str = "UTC") -> str:
    """
    Return the current date and time.

    Parameters
    ----------
    timezone : Timezone name (e.g. "UTC", "US/Eastern").
               Currently returns UTC regardless of the parameter —
               extend with the `pytz` library for real timezone support.

    Returns
    -------
    A human-readable date-time string, e.g.:
    "Monday, 2026-06-08  14:35:22 UTC"
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    return now.strftime(f"%A, %Y-%m-%d  %H:%M:%S UTC  (requested tz: {timezone})")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 3 – Web Search (stub)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@mcp.tool()
def web_search(query: str, num_results: int = 3) -> str:
    """
    Search the web for current information.

    ⚠️  STUB IMPLEMENTATION
    Replace the body of this function with a real search API call, e.g.:
      • DuckDuckGo: `from duckduckgo_search import DDGS`
      • Brave Search API: https://api.search.brave.com
      • Google Custom Search JSON API

    Parameters
    ----------
    query       : The search query string.
    num_results : How many results to return (1–10).
    """
    # TODO: Replace with real search implementation
    return (
        f"[web_search STUB]\n"
        f"Query: {query!r}\n"
        f"Results requested: {num_results}\n\n"
        f"To enable real web search, replace the body of web_search() in\n"
        f"mcp_tools/server.py with a call to DuckDuckGo or Brave Search API.\n\n"
        f"Example with duckduckgo-search:\n"
        f"  from duckduckgo_search import DDGS\n"
        f"  with DDGS() as ddgs:\n"
        f"      results = list(ddgs.text(query, max_results=num_results))\n"
        f"  return '\\n'.join(f'{{r[\"title\"]}}: {{r[\"href\"]}}' for r in results)"
    )


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Run the server over stdio (default transport for local use).
    # This is what the MCP Tool Agent spawns as a subprocess.
    mcp.run(transport="stdio")
