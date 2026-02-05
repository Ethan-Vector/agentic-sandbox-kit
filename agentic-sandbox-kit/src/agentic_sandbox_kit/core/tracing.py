from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

@dataclass
class TracingConfig:
    enabled: bool = True
    trace_dir: str = "workspace/traces"

class Tracer:
    def __init__(self, config: TracingConfig) -> None:
        self.config = config
        self.run_id = str(uuid.uuid4())
        self._path: Optional[Path] = None

    def start(self) -> None:
        if not self.config.enabled:
            return
        d = Path(self.config.trace_dir)
        d.mkdir(parents=True, exist_ok=True)
        self._path = d / f"run_{self.run_id}.jsonl"
        self._emit({"type": "run_start", "ts": time.time(), "run_id": self.run_id})

    def end(self, summary: dict[str, Any] | None = None) -> None:
        if not self.config.enabled:
            return
        self._emit({"type": "run_end", "ts": time.time(), "run_id": self.run_id, "summary": summary or {}})

    def span(self, name: str):
        return _Span(self, name)

    def event(self, event_type: str, **fields: Any) -> None:
        if not self.config.enabled:
            return
        payload = {"type": event_type, "ts": time.time(), "run_id": self.run_id}
        payload.update(fields)
        self._emit(payload)

    def _emit(self, obj: Dict[str, Any]) -> None:
        if not self._path:
            return
        with self._path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

class _Span:
    def __init__(self, tracer: Tracer, name: str) -> None:
        self.tracer = tracer
        self.name = name
        self.span_id = str(uuid.uuid4())
        self.start_ts: float | None = None

    def __enter__(self):
        self.start_ts = time.time()
        self.tracer.event("span_start", span_id=self.span_id, name=self.name)
        return self

    def __exit__(self, exc_type, exc, tb):
        end_ts = time.time()
        self.tracer.event(
            "span_end",
            span_id=self.span_id,
            name=self.name,
            duration_s=(end_ts - (self.start_ts or end_ts)),
            error=str(exc) if exc else None,
        )
        return False
