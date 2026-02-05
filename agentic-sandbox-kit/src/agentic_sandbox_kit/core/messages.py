from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

Role = Literal["system", "user", "assistant", "tool"]

@dataclass(frozen=True)
class Message:
    role: Role
    content: str

def ensure_messages(messages: Sequence[Message]) -> list[Message]:
    return list(messages)
