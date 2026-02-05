from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Sequence

from .messages import Message
from .sandbox import PolicyError, Sandbox, SandboxConfig
from .tools import ToolRegistry
from .tracing import Tracer, TracingConfig
from ..providers.base import Provider, ProviderConfig
from ..providers.factory import make_provider

class AgentError(RuntimeError):
    pass

@dataclass
class RunConfig:
    sandbox: SandboxConfig
    tracing: TracingConfig
    provider: ProviderConfig

@dataclass
class RunResult:
    final: str
    steps: int
    tool_calls: list[dict[str, Any]]
    trace_run_id: str | None = None

def _parse_action(text: str) -> dict[str, Any]:
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as e:
        raise AgentError(f"Provider returned non-JSON action: {e}") from e
    if obj.get("type") not in {"tool", "final"}:
        raise AgentError("Action JSON must include type='tool' or type='final'")
    return obj

class AgentRunner:
    def __init__(self, registry: ToolRegistry, provider: Provider, sandbox: Sandbox, tracer: Tracer) -> None:
        self.registry = registry
        self.provider = provider
        self.sandbox = sandbox
        self.tracer = tracer

    def run(self, user_input: str, system: str = "You are a helpful agent.") -> RunResult:
        start = time.time()
        self.tracer.start()

        messages: list[Message] = [Message("system", system), Message("user", user_input)]
        tool_calls: list[dict[str, Any]] = []
        final = ""
        max_steps = self.sandbox.config.max_steps

        for step in range(1, max_steps + 1):
            if time.time() - start > self.sandbox.config.max_total_time_s:
                raise AgentError("Run exceeded total time budget")

            with self.tracer.span("generate"):
                action_text = self.provider.generate(messages, self.registry.to_llm_schema(), {})
            action = _parse_action(action_text)

            if action["type"] == "final":
                final = str(action.get("content", ""))
                self.tracer.event("final", content=final)
                break

            tool_name = str(action.get("name", ""))
            args = action.get("args") or {}
            if not isinstance(args, dict):
                raise AgentError("Tool args must be an object")

            deadline = time.time() + self.sandbox.config.tool_timeout_s
            self.tracer.event("tool_call", name=tool_name, args=args, step=step)
            with self.tracer.span("tool"):
                try:
                    res = self.sandbox.call_tool(tool_name, args, deadline)
                except PolicyError as e:
                    self.tracer.event("tool_result", name=tool_name, ok=False, error=str(e), step=step)
                    messages.append(Message("assistant", json.dumps({"error": str(e)})))
                    continue

            tool_calls.append({"name": tool_name, "args": args, "ok": res.ok})
            self.tracer.event("tool_result", name=tool_name, ok=res.ok, content=res.content, step=step)

            # Feed tool result back.
            messages.append(Message("assistant", action_text))
            messages.append(Message("tool", res.content))

            # A simple fallback: if tool succeeds and we already did at least one tool, finish.
            if res.ok and step >= 2:
                final = res.content
                self.tracer.event("final", content=final)
                break

        else:
            raise AgentError("Max steps reached without final")

        summary = {
            "steps": step,
            "tool_calls": len(tool_calls),
            "duration_s": time.time() - start,
        }
        self.tracer.end(summary=summary)
        return RunResult(final=final, steps=step, tool_calls=tool_calls, trace_run_id=self.tracer.run_id)

def build_runner(cfg: RunConfig, registry: ToolRegistry) -> AgentRunner:
    provider = make_provider(cfg.provider)
    sandbox = Sandbox(cfg.sandbox, registry)
    tracer = Tracer(cfg.tracing)
    return AgentRunner(registry=registry, provider=provider, sandbox=sandbox, tracer=tracer)
