"""
mcp_server/server.py — MCP Tool Server

Registers the Calculator and Weather tools under the MCP protocol
and exposes them over stdio (standard input/output transport).

How MCP works here:
  1. This script runs as a subprocess launched by the MCP agent.
  2. The agent communicates with it over stdin/stdout (stdio transport).
  3. The @mcp.tool() decorator declares each tool — its name, description,
     and parameter schema — so the LLM knows how to call them.
  4. When the LLM decides to use a tool, MCP routes the call here,
     runs the function, and streams the result back.

Run standalone (for testing):
  python -m mcp_server.server
"""

import json
import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from mcp_server.tools.calculator import calculate
from mcp_server.tools.weather import get_weather
from config import MCP_SERVER_NAME


# ── Create MCP server instance ───────────────────────────────────────────────
mcp = Server(MCP_SERVER_NAME)


# ── Declare available tools ──────────────────────────────────────────────────

@mcp.list_tools()
async def list_tools() -> list[Tool]:
    """Tell the client which tools this server exposes."""
    return [
        Tool(
            name="calculator",
            description=(
                "Evaluate a mathematical expression and return the numeric result. "
                "Supports +, -, *, /, **, %, parentheses, and math functions like "
                "sqrt(), sin(), cos(), log(), abs(), round(), floor(), ceil(). "
                "Use for any arithmetic or math computation."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "The math expression to evaluate. "
                            "Examples: '2 + 2', 'sqrt(144)', '(3**4) / 9'"
                        ),
                    }
                },
                "required": ["expression"],
            },
        ),
        Tool(
            name="get_weather",
            description=(
                "Get the current weather conditions for a given city. "
                "Returns temperature (Celsius), humidity, wind speed, and "
                "a short description of conditions. "
                "Use for any weather, temperature, or forecast query."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": (
                            "Name of the city to check. "
                            "Examples: 'London', 'Tokyo', 'New York'"
                        ),
                    }
                },
                "required": ["city"],
            },
        ),
    ]


# ── Handle tool calls ────────────────────────────────────────────────────────

@mcp.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Dispatch an incoming tool call to the correct function.

    MCP calls this automatically when the LLM requests a tool.
    We always return a list of TextContent — MCP's standard response type.
    """

    if name == "calculator":
        expression = arguments.get("expression", "")
        result = calculate(expression)
        output = (
            f"Expression : {result['expression']}\n"
            f"Result     : {result['result']}\n"
        )
        if result["error"]:
            output += f"Error      : {result['error']}\n"

    elif name == "get_weather":
        city = arguments.get("city", "")
        result = get_weather(city)
        if result["error"]:
            output = f"Error fetching weather for '{city}': {result['error']}"
        else:
            output = (
                f"Weather in {result['city']}, {result['country']}:\n"
                f"  Temperature : {result['temperature_celsius']}°C "
                f"(feels like {result['feels_like_celsius']}°C)\n"
                f"  Humidity    : {result['humidity_percent']}%\n"
                f"  Conditions  : {result['description']}\n"
                f"  Wind speed  : {result['wind_speed_ms']} m/s\n"
                f"  Source      : {result['source']}\n"
            )

    else:
        output = f"Unknown tool: '{name}'. Available tools: calculator, get_weather."

    return [TextContent(type="text", text=output)]


# ── Entry point ──────────────────────────────────────────────────────────────

async def main():
    """Run the MCP server over stdio transport."""
    print(f"🔧 MCP Server '{MCP_SERVER_NAME}' starting (stdio transport)…")
    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(
            read_stream,
            write_stream,
            mcp.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
