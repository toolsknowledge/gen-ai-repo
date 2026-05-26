"""
MCP Server — exposes 4 tools the agent can call:
  read_file, list_files, detect_language, get_file_stats
"""
import os, json
from pathlib import Path
from typing import Any
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from loguru import logger

LANGUAGE_MAP = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
    ".java": "Java", ".c": "C", ".cpp": "C++", ".cs": "C#",
    ".go": "Go", ".rs": "Rust", ".rb": "Ruby", ".php": "PHP",
    ".swift": "Swift", ".kt": "Kotlin", ".sh": "Shell", ".sql": "SQL",
}

SAFE_BASE_DIR = Path(os.getenv("SAFE_BASE_DIR", "/tmp/code_uploads")).resolve()

def is_safe_path(path: Path) -> bool:
    try:
        path.resolve().relative_to(SAFE_BASE_DIR)
        return True
    except ValueError:
        return False

app = Server("code-review-mcp-server")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="read_file",
            description="Read full content of a code file.",
            inputSchema={"type": "object", "properties": {
                "file_path": {"type": "string"}}, "required": ["file_path"]}
        ),
        types.Tool(
            name="list_files",
            description="List all files in a directory.",
            inputSchema={"type": "object", "properties": {
                "directory": {"type": "string"},
                "recursive": {"type": "boolean", "default": False}},
                "required": ["directory"]}
        ),
        types.Tool(
            name="detect_language",
            description="Detect programming language of a file.",
            inputSchema={"type": "object", "properties": {
                "file_path": {"type": "string"}}, "required": ["file_path"]}
        ),
        types.Tool(
            name="get_file_stats",
            description="Get line count, blank lines, comments, language.",
            inputSchema={"type": "object", "properties": {
                "file_path": {"type": "string"}}, "required": ["file_path"]}
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    if name == "read_file":
        path = Path(arguments["file_path"]).resolve()
        if not is_safe_path(path):
            return [types.TextContent(type="text", text="ERROR: Access denied.")]
        if not path.exists():
            return [types.TextContent(type="text", text=f"ERROR: Not found: {path}")]
        return [types.TextContent(type="text", text=path.read_text(encoding="utf-8", errors="replace"))]

    elif name == "list_files":
        directory = Path(arguments["directory"]).resolve()
        pattern = "**/*" if arguments.get("recursive") else "*"
        files = [
            f"  {f.name} | {LANGUAGE_MAP.get(f.suffix.lower(),'Unknown')} | {f.stat().st_size/1024:.1f}KB"
            for f in directory.glob(pattern) if f.is_file()
        ]
        return [types.TextContent(type="text", text="\n".join(files) or "No files found.")]

    elif name == "detect_language":
        path = Path(arguments["file_path"])
        return [types.TextContent(type="text", text=LANGUAGE_MAP.get(path.suffix.lower(), "Unknown"))]

    elif name == "get_file_stats":
        path = Path(arguments["file_path"]).resolve()
        if not is_safe_path(path):
            return [types.TextContent(type="text", text="ERROR: Access denied.")]
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        total = len(lines)
        blank = sum(1 for l in lines if not l.strip())
        comments = sum(1 for l in lines if l.strip().startswith(("#","//","/*","*","--")))
        stats = {"total_lines": total, "code_lines": total-blank-comments,
                 "blank_lines": blank, "comment_lines": comments,
                 "language": LANGUAGE_MAP.get(path.suffix.lower(), "Unknown")}
        return [types.TextContent(type="text", text=json.dumps(stats, indent=2))]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())