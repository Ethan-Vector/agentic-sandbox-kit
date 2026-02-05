from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core.agent import RunConfig, build_runner
from .core.sandbox import SandboxConfig
from .core.tracing import TracingConfig
from .providers.base import ProviderConfig
from .tools import build_default_registry
from .evals.harness import run_eval
from .trace.report import summarize_trace_dir, to_dict

def _load_cfg(path: str | None) -> RunConfig:
    if path is None:
        path = "configs/config.example.json"
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    s = obj.get("sandbox") or {}
    t = obj.get("tracing") or {}
    p = obj.get("provider") or {}
    return RunConfig(
        sandbox=SandboxConfig(
            workspace_dir=s.get("workspace_dir", "workspace"),
            max_steps=int(s.get("max_steps", 8)),
            tool_timeout_s=float(s.get("tool_timeout_s", 3)),
            max_total_time_s=float(s.get("max_total_time_s", 12)),
            allowed_tools=list(s.get("allowed_tools") or []),
        ),
        tracing=TracingConfig(
            enabled=bool(t.get("enabled", True)),
            trace_dir=str(t.get("trace_dir", "workspace/traces")),
        ),
        provider=ProviderConfig(type=str(p.get("type", "mock")), model=p.get("model")),
    )

def cmd_run(args: argparse.Namespace) -> int:
    cfg = _load_cfg(args.config)
    reg = build_default_registry()
    runner = build_runner(cfg, reg)
    r = runner.run(args.input)
    print(r.final)
    return 0

def cmd_demo(args: argparse.Namespace) -> int:
    demo = json.loads(Path("scenarios/demo.json").read_text(encoding="utf-8"))
    args.input = demo["input"]
    return cmd_run(args)

def cmd_eval(args: argparse.Namespace) -> int:
    summary = run_eval(args.dataset)
    print(json.dumps(summary, indent=2))
    return 0 if summary["passed"] == summary["total"] else 1

def cmd_trace_report(args: argparse.Namespace) -> int:
    s = summarize_trace_dir(args.trace_dir)
    print(json.dumps(to_dict(s), indent=2))
    return 0

def main() -> None:
    p = argparse.ArgumentParser(prog="askit", description="Agentic Sandbox Kit CLI")
    p.add_argument("--config", default=None, help="Path to config JSON (default: configs/config.example.json)")
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("run", help="Run a single agent session")
    pr.add_argument("--input", required=True, help="User prompt")
    pr.set_defaults(func=cmd_run)

    pd = sub.add_parser("demo", help="Run the demo scenario")
    pd.set_defaults(func=cmd_demo)

    pe = sub.add_parser("eval", help="Run eval harness")
    pe.add_argument("--dataset", default="evals/datasets/smoke.jsonl", help="Path to JSONL dataset")
    pe.set_defaults(func=cmd_eval)

    pt = sub.add_parser("trace", help="Trace utilities")
    tsub = pt.add_subparsers(dest="trace_cmd", required=True)
    ptr = tsub.add_parser("report", help="Summarize traces in a directory")
    ptr.add_argument("--trace-dir", default="workspace/traces")
    ptr.set_defaults(func=cmd_trace_report)

    args = p.parse_args()
    raise SystemExit(args.func(args))

if __name__ == "__main__":
    main()
