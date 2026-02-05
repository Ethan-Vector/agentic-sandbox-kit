from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass
class TraceSummary:
    runs: int
    tool_calls: int
    durations: list[float]

def summarize_trace_dir(trace_dir: str) -> TraceSummary:
    d = Path(trace_dir)
    if not d.exists():
        return TraceSummary(runs=0, tool_calls=0, durations=[])
    tool_calls = 0
    durations: list[float] = []
    runs = 0
    for p in d.glob("run_*.jsonl"):
        runs += 1
        run_dur = None
        for line in p.read_text(encoding="utf-8").splitlines():
            obj = json.loads(line)
            if obj.get("type") == "tool_call":
                tool_calls += 1
            if obj.get("type") == "run_end":
                run_dur = (obj.get("summary") or {}).get("duration_s")
        if isinstance(run_dur, (int, float)):
            durations.append(float(run_dur))
    return TraceSummary(runs=runs, tool_calls=tool_calls, durations=durations)

def pct(values: list[float], p: float) -> float | None:
    if not values:
        return None
    v = sorted(values)
    k = int(round((len(v) - 1) * p))
    return v[max(0, min(k, len(v) - 1))]

def to_dict(s: TraceSummary) -> dict[str, Any]:
    return {
        "runs": s.runs,
        "tool_calls": s.tool_calls,
        "duration_p50_s": pct(s.durations, 0.50),
        "duration_p95_s": pct(s.durations, 0.95),
        "duration_p99_s": pct(s.durations, 0.99),
    }
