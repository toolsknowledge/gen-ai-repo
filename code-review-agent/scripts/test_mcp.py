import asyncio, sys
sys.path.insert(0, ".")
from backend.mcp_client.client import CodeReviewMCPClient

async def main():
    async with CodeReviewMCPClient() as client:
        tools = await client.list_available_tools()
        print("Tools:", tools)
        lang = await client.call_tool("detect_language", {"file_path": "/tmp/code_uploads/test_vuln.py"})
        print("Language:", lang)
        stats = await client.call_tool("get_file_stats", {"file_path": "/tmp/code_uploads/test_vuln.py"})
        print("Stats:", stats)

asyncio.run(main())