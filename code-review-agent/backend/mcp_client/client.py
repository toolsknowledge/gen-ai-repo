"""
MCP Client — connects the agent to the MCP Server tools.
"""
from typing import Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from loguru import logger


class CodeReviewMCPClient:
    def __init__(self, server_script: str = "backend/mcp_server/server.py"):
        self.server_script = server_script
        self._session = None
        self._context = None

    async def __aenter__(self):
        server_params = StdioServerParameters(command="python", args=[self.server_script])
        self._context = stdio_client(server_params)
        read, write = await self._context.__aenter__()
        self._session = ClientSession(read, write)
        await self._session.__aenter__()
        await self._session.initialize()
        logger.info("MCP Client connected.")
        return self

    async def __aexit__(self, *args):
        if self._session:
            await self._session.__aexit__(*args)
        if self._context:
            await self._context.__aexit__(*args)

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        result = await self._session.call_tool(tool_name, arguments)
        return "\n".join(c.text for c in result.content if hasattr(c, "text"))

    async def list_available_tools(self) -> list[str]:
        tools = await self._session.list_tools()
        return [t.name for t in tools.tools]