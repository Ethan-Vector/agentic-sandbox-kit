from __future__ import annotations

from .base import Provider, ProviderConfig
from .mock import MockLLM

def make_provider(cfg: ProviderConfig) -> Provider:
    if cfg.type == "mock":
        return MockLLM()
    raise ValueError(f"Unknown provider type: {cfg.type}")
