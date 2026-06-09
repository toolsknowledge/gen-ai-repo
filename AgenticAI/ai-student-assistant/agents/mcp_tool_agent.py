"""
agents/mcp_tool_agent.py
────────────────────────
The MCP Tool Agent: decides which MCP tools to call and executes them.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT DOES THIS AGENT DO?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The Supervisor routes here when the query needs external tools
(calculations, dates, web searches).

This agent:
  1. Connects to the MCP server (mcp_tools/server.py) via stdio.
  2. Asks the LLM "which tool should I call for this query?" using
     Claude's native tool_use capability.
  3. Executes the chosen tool via MCP.
  4. Writes the results to state["tool_results"].

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MCP COMMUNICATION FLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  This Agent (MCP client)                 mcp_tools/server.py (MCP server)
       │                                          │
       │──── spawn subprocess ─────────────────►  │  (server starts, listens on stdin)
       │                                          │
       │──── tools/list ──────────────────────►   │
       │◄─── [calculate, get_current_date, ...] ──│
       │                                          │
       │──── tools/call {"name": "calculate"} ──► │
       │◄─── {"result": "42"} ────────────────────│
       │                                          │
       │──── subprocess kill ──────────────────►  │

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHY USE THE LLM TO DECIDE WHICH TOOL TO CALL?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
We could hardcode rules ("if query contains 'calculate' → call calculate"),
but that breaks for anything phrased differently.

Instead we give Claude the list of available MCP tools and let it pick.
This is Claude's native "tool_use" feature – the same mechanism used by
Claude in production for function calling.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from anthropic import Anthropic

from agents.base_agent import BaseAgent
from graph.state import AgentState
from config import settings
from utils.logger import get_logger

log = get_logger(__name__)

# Path to the MCP server script
MCP_SERVER_SCRIPT = str(Path(__file__).parent.parent / "mcp_tools" / "server.py")


class MCPToolAgent(BaseAgent):
    """
    Uses Claude's tool_use to select and call MCP tools.

    We use the raw Anthropic SDK here (not LangChain) because the native
    Anthropic SDK provides the cleanest interface for tool_use messages.
    LangChain wraps this but adds complexity for what is a straightforward
    tool-use loop.
    """

    def __init__(self) -> None:
        super().__init__("MCPToolAgent")
        self._client = Anthropic(api_key=settings.anthropic_api_key)

    # ── Core logic ────────────────────────────────────────────────────────────

    def _execute(self, state: AgentState) -> AgentState:
        """
        Decide which tools to call and execute them via MCP.

        Uses asyncio.run() because MCP client is async.
        """
        result = asyncio.run(self._async_execute(state))
        return result

    async def _async_execute(self, state: AgentState) -> AgentState:
        query = state["query"]

        # ── Import MCP client ─────────────────────────────────────────────────
        # We import here (not at module level) to avoid import errors if
        # the MCP library isn't installed.
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
        except ImportError:
            log.error("MCP library not installed. Run: pip install mcp")
            return {                                         # type: ignore
                "tool_results": {"error": "MCP library not available"},
            }

        log.info("Connecting to MCP server: %s", MCP_SERVER_SCRIPT)

        server_params = StdioServerParameters(
            command=sys.executable,      # same Python interpreter
            args=[MCP_SERVER_SCRIPT],
            env=None,
        )

        tool_results: dict[str, Any] = {}

        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # ── 1. Discover available tools ───────────────────────────
                    await session.initialize()
                    tools_response = await session.list_tools()

                    # Convert MCP tool definitions to Anthropic tool format
                    anthropic_tools = []
                    for tool in tools_response.tools:
                        anthropic_tools.append({
                            "name": tool.name,
                            "description": tool.description or "",
                            "input_schema": tool.inputSchema or {
                                "type": "object",
                                "properties": {},
                            },
                        })

                    log.info("Available MCP tools: %s",
                             [t["name"] for t in anthropic_tools])

                    # ── 2. Ask Claude which tool(s) to call ───────────────────
                    messages = [
                        {
                            "role": "user",
                            "content": (
                                f"The user asked: {query!r}\n\n"
                                "Use the available tools to help answer this question. "
                                "Call one or more tools as needed."
                            ),
                        }
                    ]

                    response = self._client.messages.create(
                        model=settings.claude_fast_model,
                        max_tokens=512,
                        tools=anthropic_tools,
                        messages=messages,
                    )

                    # ── 3. Execute each tool Claude chose ─────────────────────
                    # Process tool_use blocks in the response
                    for block in response.content:
                        if block.type != "tool_use":
                            continue

                        tool_name = block.name
                        tool_input = block.input  # dict of arguments

                        log.info("Calling MCP tool: %s(%s)",
                                 tool_name, json.dumps(tool_input))

                        # Call the MCP server tool
                        call_result = await session.call_tool(
                            tool_name, arguments=tool_input
                        )

                        # Extract text content from the MCP result
                        result_text = ""
                        for content in call_result.content:
                            if hasattr(content, "text"):
                                result_text += content.text

                        tool_results[tool_name] = result_text
                        log.info("  %s → %s", tool_name,
                                 result_text[:80] + "…" if len(result_text) > 80
                                 else result_text)

                    # If Claude didn't call any tools, record that
                    if not tool_results:
                        tool_results["info"] = (
                            "No tools were called. The query may not require "
                            "external tool assistance."
                        )

        except Exception as exc:
            log.error("MCP error: %s", exc, exc_info=True)
            tool_results["error"] = str(exc)

        return {                                             # type: ignore
            "tool_results": tool_results,
            "history": [{
                "role": "system",
                "content": f"MCPToolAgent: called {list(tool_results.keys())}",
            }],
        }


# ── Singleton ─────────────────────────────────────────────────────────────────
mcp_tool_agent = MCPToolAgent()
