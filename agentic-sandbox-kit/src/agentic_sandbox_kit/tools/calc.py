from __future__ import annotations

import ast
import operator
import time
from typing import Any

from ..core.tools import Tool, ToolContext, ToolResult

_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        return _ALLOWED_BINOPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY:
        return _ALLOWED_UNARY[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")

def calc_tool(args: dict, ctx: ToolContext) -> ToolResult:
    expr = str(args.get("expression", "")).strip()
    if not expr:
        return ToolResult(ok=False, content="Missing 'expression'")
    # deadline check (cheap)
    if time.time() > ctx.deadline:
        return ToolResult(ok=False, content="Timeout")
    try:
        tree = ast.parse(expr, mode="eval")
        val = _eval(tree)
        if val.is_integer():
            out = str(int(val))
        else:
            out = str(val)
        return ToolResult(ok=True, content=out, metadata={"expression": expr})
    except Exception as e:
        return ToolResult(ok=False, content=f"Calc error: {e}")

TOOL = Tool(
    name="calc",
    description="Safely evaluate a basic arithmetic expression (e.g., '19*7', '2+2').",
    fn=calc_tool,
)
