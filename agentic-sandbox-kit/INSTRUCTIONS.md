# How to use this repo (practical workflow)

## 1) Pick your sandbox policy
Edit `configs/config.example.json`:
- allowlisted tools
- max steps
- max wall time per tool
- workspace dir

## 2) Add tools safely
Tools live in `src/agentic_sandbox_kit/tools/`.
Rules of thumb:
- deterministic, side-effect controlled
- explicit allowlists
- never accept raw shell commands

Read: `docs/ADDING_TOOLS.md`.

## 3) Add your provider
The default provider is `MockLLM` (offline).
To plug in a real LLM, implement `Provider.generate()` and wire it in `providers/`.

Read: `docs/ADDING_A_PROVIDER.md`.

## 4) Add scenarios + evals
- scenarios are JSON files under `scenarios/`
- eval datasets are JSONL under `evals/datasets/`

Run:
```bash
askit eval
```

## 5) Ship confidently
Before you publish or expose the agent:
- lock allowlists
- set budgets
- run evals in CI
- keep traces for incident reviews
