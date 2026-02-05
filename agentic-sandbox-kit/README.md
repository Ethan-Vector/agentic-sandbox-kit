# agentic-sandbox-kit

A small, **production-friendly starter kit** for building and testing agentic workflows:
- tool calling (OpenAI-style `tool` / `final`)
- guardrails (allowlists, budgets, timeouts)
- traces (JSONL spans)
- eval harness (offline, deterministic)
- a minimal CLI you can extend

This repo is intentionally **offline-first**: it ships with a deterministic `MockLLM` so CI runs without API keys.
You can plug in a real provider later.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
askit demo
askit eval
```

## What you get

- `src/agentic_sandbox_kit/`
  - `core/agent.py` – the agent loop
  - `core/tools.py` – tool protocol + registry
  - `core/sandbox.py` – budgets, allowlists, workspace isolation
  - `core/tracing.py` – JSONL traces with spans
  - `providers/mock.py` – deterministic LLM for local + CI
- `scenarios/` – ready-to-run tasks
- `evals/` – harness + tiny datasets
- `tests/` – smoke and unit tests
- `configs/` – example configuration
- `.github/workflows/ci.yml` – ruff + pytest + evals
- `Dockerfile` / `docker-compose.yml`

## CLI

```bash
askit demo                     # run a demo scenario
askit run --input "..."         # run a single prompt
askit eval                      # run evaluation suite
askit trace report              # summarize traces (p50/p95, tool usage)
```

## Extending

Start with `docs/ADDING_TOOLS.md` and `docs/ADDING_A_PROVIDER.md`.

## License

MIT. See `LICENSE`.
