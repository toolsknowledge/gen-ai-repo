"""
agents/mcp_agent.py — MCP Tool Agent

How this agent works:
  1. Use Claude's tool_use API to let Claude decide which tool to call
     (calculator or get_weather) based on the user's query.
  2. Extract the tool name + arguments from Claude's response.
  3. Execute the tool locally (direct function call — fast, no subprocess needed
     for simple use; the MCP server pattern is shown in server.py for network use).
  4. Send the tool result back to Claude so it can craft a natural-language answer.
  5. Return final response + raw tool result.

Why direct function calls here?
  The MCP server (server.py) is the production pattern for networked,
  multi-client tool serving. For a single-app workflow, calling the tool
  functions directly keeps things simple and avoids subprocess management.
  Both patterns are architecturally valid — this agent shows the LLM-tool
  interaction loop clearly.
"""

import json
from typing import Any

from anthropic import Anthropic

from config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from mcp_server.tools.calculator import calculate
from mcp_server.tools.weather import get_weather

# ── Anthropic client ──────────────────────────────────────────────────────────
_client = Anthropic(api_key=ANTHROPIC_API_KEY)

# ── Tool definitions for Claude's tool_use API ────────────────────────────────
# These mirror the MCP tool schemas in server.py so Claude knows what's available.
TOOLS = [
    {
        "name": "calculator",
        "description": (
            "Evaluate a mathematical expression and return the numeric result. "
            "Supports +, -, *, /, **, %, parentheses, sqrt(), sin(), cos(), "
            "log(), abs(), round(), floor(), ceil(), pi, e. "
            "Use for any arithmetic or math computation."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression, e.g. '2 + 2', 'sqrt(144)', '(3**4)/9'",
                }
            },
            "required": ["expression"],
        },
    },
    {
        "name": "get_weather",
        "description": (
            "Get current weather for a city: temperature, humidity, wind, conditions. "
            "Use for any weather, temperature, or forecast question."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g. 'London', 'Tokyo', 'New York'",
                }
            },
            "required": ["city"],
        },
    },
]


def _execute_tool(tool_name: str, tool_input: dict) -> str:
    """
    Dispatch a tool call to the correct function and return a string result.

    Parameters
    ----------
    tool_name  : str  — "calculator" or "get_weather"
    tool_input : dict — arguments as decided by Claude

    Returns
    -------
    str — formatted tool output to feed back to Claude
    """
    if tool_name == "calculator":
        result = calculate(tool_input.get("expression", ""))
        if result["error"]:
            return f"Error: {result['error']}"
        return f"Expression: {result['expression']}\nResult: {result['result']}"

    elif tool_name == "get_weather":
        result = get_weather(tool_input.get("city", ""))
        if result["error"]:
            return f"Error: {result['error']}"
        return (
            f"Weather in {result['city']}, {result['country']}:\n"
            f"  Temperature : {result['temperature_celsius']}°C "
            f"(feels like {result['feels_like_celsius']}°C)\n"
            f"  Humidity    : {result['humidity_percent']}%\n"
            f"  Conditions  : {result['description']}\n"
            f"  Wind speed  : {result['wind_speed_ms']} m/s\n"
            f"  Data source : {result['source']}"
        )

    return f"Unknown tool: {tool_name}"


def run_mcp_agent(query: str) -> dict[str, Any]:
    """
    Execute the MCP tool pipeline for a user query.

    Steps
    -----
    1. Send query + tool definitions to Claude → Claude picks a tool
    2. Extract tool_name + tool_input from Claude's tool_use block
    3. Call the tool function directly
    4. Send tool result back to Claude for a natural-language answer
    5. Return response + raw tool_result

    Parameters
    ----------
    query : str — the user's question

    Returns
    -------
    dict with keys:
        "response"    : str — Claude's final natural-language answer
        "tool_result" : str — raw output from the tool (for display)
    """
    print(f"\n🔧 MCP Agent: processing query → '{query[:80]}…'")

    # ── Step 1: Ask Claude which tool to use ──────────────────────────────────
    print(f"  🤖 Calling Claude ({CLAUDE_MODEL}) with {len(TOOLS)} tools …")

    first_response = _client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=512,
        tools=TOOLS,
        messages=[{"role": "user", "content": query}],
    )

    # ── Step 2: Check if Claude wants to use a tool ───────────────────────────
    tool_result_text = ""

    if first_response.stop_reason == "tool_use":
        # Find the tool_use block in the response
        tool_use_block = next(
            (block for block in first_response.content if block.type == "tool_use"),
            None,
        )

        if tool_use_block:
            tool_name  = tool_use_block.name
            tool_input = tool_use_block.input
            tool_use_id = tool_use_block.id

            print(f"  🛠  Claude chose tool: '{tool_name}' with input: {tool_input}")

            # ── Step 3: Execute the tool ──────────────────────────────────────
            tool_result_text = _execute_tool(tool_name, tool_input)
            print(f"  📊 Tool result:\n{tool_result_text}")

            # ── Step 4: Send tool result back to Claude ───────────────────────
            final_response = _client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1024,
                tools=TOOLS,
                messages=[
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": first_response.content},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use_id,
                                "content": tool_result_text,
                            }
                        ],
                    },
                ],
            )

            response_text = final_response.content[0].text
            print(f"  ✅ MCP Agent complete. ({final_response.usage.output_tokens} output tokens)")

        else:
            response_text = "Claude requested tool use but no tool_use block was found."

    else:
        # Claude answered directly without tools (rare for tool-trigger queries)
        response_text = first_response.content[0].text
        print("  ℹ️  Claude answered directly (no tool call).")

    return {
        "response": response_text,
        "tool_result": tool_result_text,
    }
