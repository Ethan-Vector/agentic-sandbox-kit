from __future__ import annotations

import json
import re
from typing import Sequence

from ..core.messages import Message
from .base import Provider

class MockLLM(Provider):
    """
    Deterministic provider used for offline runs and CI.

    It emits an action JSON string. Heuristics:
    - if prompt contains 'calculate' or a simple math expression -> calc
    - if it contains 'write' and a filename -> write_file
    - if it contains 'read' and a filename -> read_file
    - else -> final with a short response
    """

    def generate(self, messages: Sequence[Message], tools: list[dict], config: dict) -> str:
        user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        # read requests
        m = re.search(r"read\s+([\w\-/\.]+)", user, flags=re.I)
        if m:
            return json.dumps({"type": "tool", "name": "read_file", "args": {"path": m.group(1)}})
        # write requests
        m = re.search(r"(write|save).*(?:file\s+named\s+|to\s+)([\w\-/\.]+)", user, flags=re.I)
        if m:
            # If user asked to calculate too, do calc first; agent loop will handle.
            content = re.sub(r"\s+", " ", user).strip()
            return json.dumps({"type": "tool", "name": "note_append", "args": {"path": m.group(2), "text": content}})
        # calc: try to extract expression like 19*7
        expr = None
        m = re.search(r"calculate\s+([^\n\r]+)", user, flags=re.I)
        if m:
            expr = m.group(1).strip()
        else:
            m = re.search(r"(\d+\s*[\+\-\*/]\s*\d+)", user)
            if m:
                expr = m.group(1).strip()
        if expr:
            return json.dumps({"type": "tool", "name": "calc", "args": {"expression": expr}})
        return json.dumps({"type": "final", "content": "OK. (MockLLM) No tool needed for this request."})
