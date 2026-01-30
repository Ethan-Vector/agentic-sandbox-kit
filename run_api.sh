#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=./src
export CONFIG_PATH="${CONFIG_PATH:-configs/policies.yaml}"
uvicorn agentic_sandbox.api:app --host "${APP_HOST:-0.0.0.0}" --port "${APP_PORT:-8095}" --reload
