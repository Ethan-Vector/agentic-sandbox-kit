.PHONY: dev test lint fmt

dev:
	uvicorn agentic_sandbox.api:app --host 0.0.0.0 --port 8095 --reload

test:
	pytest -q

lint:
	ruff check .
	mypy src

fmt:
	ruff format .
