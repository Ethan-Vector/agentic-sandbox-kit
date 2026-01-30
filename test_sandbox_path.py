from agentic_sandbox.config import SandboxConfig
from agentic_sandbox.sandbox import Sandbox
from agentic_sandbox.errors import ToolError

def test_path_traversal_denied(tmp_path):
    sb = Sandbox(SandboxConfig(root_dir=str(tmp_path)))
    try:
        sb.resolve_path("../etc/passwd")
        assert False
    except ToolError:
        assert True
