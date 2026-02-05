from __future__ import annotations

from ..core.tools import ToolRegistry
from .calc import TOOL as CALC
from .note import TOOL as NOTE_APPEND
from .files import READ_TOOL, WRITE_TOOL, LIST_TOOL
from .echo import TOOL as ECHO

def build_default_registry() -> ToolRegistry:
    reg = ToolRegistry()
    for t in [CALC, NOTE_APPEND, READ_TOOL, WRITE_TOOL, LIST_TOOL, ECHO]:
        reg.register(t)
    return reg
