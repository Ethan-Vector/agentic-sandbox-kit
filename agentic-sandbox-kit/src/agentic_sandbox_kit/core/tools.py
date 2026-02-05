from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

@dataclass
class ToolResult:
    ok: bool
    content: str
    metadata: Dict[str, Any] | None = None

@dataclass
class ToolContext:
    workspace: "Workspace"
    # epoch seconds
    deadline: float

ToolFn = Callable[[dict, ToolContext], ToolResult]

@dataclass
class Tool:
    name: str
    description: str
    fn: ToolFn

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def list(self) -> list[Tool]:
        return list(self._tools.values())

    def to_llm_schema(self) -> list[dict]:
        # Minimal schema used by providers; extend as needed.
        return [{"name": t.name, "description": t.description} for t in self.list()]

# Forward-declared to avoid import cycles (runtime import in sandbox.py)
class Workspace:  # pragma: no cover
    ...
