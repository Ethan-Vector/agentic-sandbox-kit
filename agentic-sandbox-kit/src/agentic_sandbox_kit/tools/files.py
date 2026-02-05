from __future__ import annotations

import time
from ..core.tools import Tool, ToolContext, ToolResult

def read_file(args: dict, ctx: ToolContext) -> ToolResult:
    path = str(args.get("path", "")).strip()
    if not path:
        return ToolResult(ok=False, content="Missing 'path'")
    if time.time() > ctx.deadline:
        return ToolResult(ok=False, content="Timeout")
    try:
        return ToolResult(ok=True, content=ctx.workspace.read_text(path))
    except Exception as e:
        return ToolResult(ok=False, content=f"Read error: {e}")

def write_file(args: dict, ctx: ToolContext) -> ToolResult:
    path = str(args.get("path", "")).strip()
    text = str(args.get("text", ""))
    if not path:
        return ToolResult(ok=False, content="Missing 'path'")
    if time.time() > ctx.deadline:
        return ToolResult(ok=False, content="Timeout")
    try:
        ctx.workspace.write_text(path, text)
        return ToolResult(ok=True, content=f"Wrote {len(text)} bytes to {path}")
    except Exception as e:
        return ToolResult(ok=False, content=f"Write error: {e}")

def list_files(args: dict, ctx: ToolContext) -> ToolResult:
    rel = str(args.get("dir", ".")).strip() or "."
    if time.time() > ctx.deadline:
        return ToolResult(ok=False, content="Timeout")
    try:
        files = ctx.workspace.list_files(rel)
        return ToolResult(ok=True, content="\n".join(files))
    except Exception as e:
        return ToolResult(ok=False, content=f"List error: {e}")

READ_TOOL = Tool(
    name="read_file",
    description="Read a text file from the workspace. Args: {path}.",
    fn=read_file,
)
WRITE_TOOL = Tool(
    name="write_file",
    description="Write a text file inside the workspace. Args: {path, text}.",
    fn=write_file,
)
LIST_TOOL = Tool(
    name="list_files",
    description="List files in the workspace. Args: {dir} optional.",
    fn=list_files,
)
