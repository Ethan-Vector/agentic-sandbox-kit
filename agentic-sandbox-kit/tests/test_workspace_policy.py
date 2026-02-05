import time
import pytest
from agentic_sandbox_kit.core.sandbox import Workspace, PolicyError
from agentic_sandbox_kit.core.tools import ToolContext
from agentic_sandbox_kit.tools.files import read_file

def test_workspace_escape_blocked(tmp_path):
    ws = Workspace(str(tmp_path / "ws"))
    ctx = ToolContext(workspace=ws, deadline=time.time() + 5)
    # Try to escape (should fail)
    r = read_file({"path": "../secret.txt"}, ctx)
    assert not r.ok

def test_resolve_inside_blocks(tmp_path):
    ws = Workspace(str(tmp_path / "ws"))
    with pytest.raises(PolicyError):
        ws.resolve_inside("../x")
