from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ..core.messages import Message

@dataclass
class ProviderConfig:
    type: str
    model: str | None = None

class Provider:
    def generate(self, messages: Sequence[Message], tools: list[dict], config: dict) -> str:
        raise NotImplementedError
