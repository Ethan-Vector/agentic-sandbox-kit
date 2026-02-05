from __future__ import annotations

import time
from ..core.tools import Tool, ToolContext, ToolResult

def note_append(args: dict, ctx: ToolContext) -> ToolResult:
    path = str(args.get("path", "notes.txt")).strip() or "notes.txt"
    text = str(args.get("text", ""))
    if time.time() > ctx.deadline:
        return ToolResult(ok=False, content="Timeout")
    try:
        existing = ""
        try:
            existing = ctx.workspace.read_text(path)
        except Exception:
            existing = ""
        new = (existing + ("\n" if existing else "") + text).strip() + "\n"
        ctx.workspace.write_text(path, new)
        return ToolResult(ok=True, content=f"Appended {len(text)} chars to {path}")
    except Exception as e:
        return ToolResult(ok=False, content=f"Note error: {e}")

TOOL = Tool(
    name="note_append",
    description="Append text to a note file in workspace. Args: {path, text}.",
    fn=note_append,
)
