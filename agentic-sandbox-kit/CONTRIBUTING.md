# Contributing

## Dev setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Style
- ruff for linting
- keep tools deterministic for CI
- add tests for every tool and policy

## PR checklist
- tests pass
- eval harness passes
- docs updated if behavior changes
