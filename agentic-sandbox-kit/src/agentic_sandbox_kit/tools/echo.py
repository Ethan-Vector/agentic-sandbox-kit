from __future__ import annotations

import time
from ..core.tools import Tool, ToolContext, ToolResult

def echo(args: dict, ctx: ToolContext) -> ToolResult:
    if time.time() > ctx.deadline:
        return ToolResult(ok=False, content="Timeout")
    return ToolResult(ok=True, content=str(args.get("text", "")))

TOOL = Tool(
    name="echo",
    description="Echo back the provided text. Args: {text}.",
    fn=echo,
)
