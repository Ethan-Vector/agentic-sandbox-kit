from agentic_sandbox.tokens import TokenCodec
from agentic_sandbox.errors import AuthError

def test_token_roundtrip():
    c = TokenCodec("secret")
    t = c.mint("alice", ["tool.fs.read"], 3600)
    cap = c.parse(t)
    assert cap.sub == "alice"
    assert "tool.fs.read" in cap.scopes

def test_token_bad_signature():
    c = TokenCodec("secret")
    t = c.mint("alice", ["x"], 3600)
    # change secret -> should fail
    c2 = TokenCodec("other")
    try:
        c2.parse(t)
        assert False
    except AuthError:
        assert True
