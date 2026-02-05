from agentic_sandbox_kit.tools.calc import calc_tool
from agentic_sandbox_kit.core.tools import ToolContext
from agentic_sandbox_kit.core.sandbox import Workspace
import time

def test_calc_mul():
    ctx = ToolContext(workspace=Workspace("workspace_test"), deadline=time.time() + 5)
    r = calc_tool({"expression": "19*7"}, ctx)
    assert r.ok
    assert r.content == "133"
