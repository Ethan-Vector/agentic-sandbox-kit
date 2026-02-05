from __future__ import annotations

def contains_expected(output: str, expected: str) -> bool:
    return expected.strip().lower() in output.strip().lower()
