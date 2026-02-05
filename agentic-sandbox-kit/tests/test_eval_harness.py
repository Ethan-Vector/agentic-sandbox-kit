from agentic_sandbox_kit.evals.harness import run_eval

def test_eval_smoke_passes():
    s = run_eval("evals/datasets/smoke.jsonl")
    assert s["total"] >= 1
    assert s["passed"] >= 1
