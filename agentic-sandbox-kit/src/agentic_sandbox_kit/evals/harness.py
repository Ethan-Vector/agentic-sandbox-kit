from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .metrics import contains_expected
from ..core.agent import RunConfig, build_runner
from ..core.sandbox import SandboxConfig
from ..core.tracing import TracingConfig
from ..providers.base import ProviderConfig
from ..tools import build_default_registry

@dataclass
class EvalCase:
    id: str
    input: str
    expected_substring: str

def load_jsonl(path: str) -> list[EvalCase]:
    out: list[EvalCase] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        out.append(EvalCase(id=obj["id"], input=obj["input"], expected_substring=obj["expected_substring"]))
    return out

def run_eval(dataset_path: str = "evals/datasets/smoke.jsonl") -> dict[str, Any]:
    registry = build_default_registry()
    cfg = RunConfig(
        sandbox=SandboxConfig(
            workspace_dir="workspace",
            max_steps=8,
            tool_timeout_s=3,
            max_total_time_s=12,
            allowed_tools=["calc", "note_append", "read_file", "write_file", "list_files", "echo"],
        ),
        tracing=TracingConfig(enabled=True, trace_dir="workspace/traces"),
        provider=ProviderConfig(type="mock", model="mock:deterministic-v1"),
    )
    runner = build_runner(cfg, registry)

    cases = load_jsonl(dataset_path)
    passed = 0
    results = []
    for c in cases:
        r = runner.run(c.input)
        ok = contains_expected(r.final, c.expected_substring)
        results.append({"id": c.id, "ok": ok, "final": r.final, "trace_run_id": r.trace_run_id})
        passed += 1 if ok else 0

    return {"passed": passed, "total": len(cases), "results": results}

if __name__ == "__main__":
    summary = run_eval()
    print(json.dumps(summary, indent=2))
    if summary["passed"] != summary["total"]:
        raise SystemExit(1)
