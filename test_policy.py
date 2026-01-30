from agentic_sandbox.config import load_config
from agentic_sandbox.tokens import TokenCodec
from agentic_sandbox.policy import check_policy

def test_policy_denies_missing_scope(tmp_path):
    cfg_text = '''
routes:
  default: {allowed_tools: ["fs.read"]}
tools:
  fs.read: {required_scopes: ["tool.fs.read"]}
'''
    p = tmp_path / "c.yaml"
    p.write_text(cfg_text)
    cfg = load_config(str(p))

    codec = TokenCodec("secret")
    cap = codec.parse(codec.mint("u", [], 3600))
    d = check_policy(cfg, cap, "default", "fs.read")
    assert d.ok is False
    assert d.reason == "missing_scope"
