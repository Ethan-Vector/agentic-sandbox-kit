from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .tools import ToolContext, ToolResult, ToolRegistry

class PolicyError(RuntimeError):
    pass

@dataclass
class SandboxConfig:
    workspace_dir: str = "workspace"
    max_steps: int = 8
    tool_timeout_s: float = 3.0
    max_total_time_s: float = 12.0
    allowed_tools: list[str] | None = None

class Workspace:
    def __init__(self, root: str) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def resolve_inside(self, relative_path: str) -> Path:
        p = (self.root / relative_path).resolve()
        if self.root not in p.parents and p != self.root:
            raise PolicyError("Path escapes workspace")
        return p

    def write_text(self, relative_path: str, text: str) -> None:
        p = self.resolve_inside(relative_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def read_text(self, relative_path: str) -> str:
        p = self.resolve_inside(relative_path)
        return p.read_text(encoding="utf-8")

    def list_files(self, relative_dir: str = ".") -> list[str]:
        d = self.resolve_inside(relative_dir)
        if not d.exists():
            return []
        return sorted([str(p.relative_to(self.root)) for p in d.rglob("*") if p.is_file()])

class Sandbox:
    def __init__(self, config: SandboxConfig, registry: ToolRegistry) -> None:
        self.config = config
        self.registry = registry
        self.workspace = Workspace(config.workspace_dir)
        self.allowed = set(config.allowed_tools or [])

    def _enforce_allowed(self, tool_name: str) -> None:
        if self.allowed and tool_name not in self.allowed:
            raise PolicyError(f"Tool not allowed: {tool_name}")

    def call_tool(self, tool_name: str, args: dict, deadline: float) -> ToolResult:
        self._enforce_allowed(tool_name)
        tool = self.registry.get(tool_name)
        if tool is None:
            raise PolicyError(f"Unknown tool: {tool_name}")
        ctx = ToolContext(workspace=self.workspace, deadline=deadline)
        # Tool is responsible for respecting deadline in long work;
        # we enforce a hard stop by checking before/after.
        start = time.time()
        res = tool.fn(args, ctx)
        elapsed = time.time() - start
        if elapsed > self.config.tool_timeout_s + 0.25:
            raise PolicyError(f"Tool exceeded timeout budget: {tool_name} ({elapsed:.2f}s)")
        return res
