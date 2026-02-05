# Trace schema (JSONL)

Each run produces a file in `workspace/traces/` with JSONL entries.

Events:
- `run_start`, `run_end`
- `span_start`, `span_end`
- `tool_call`, `tool_result`
- `final`

Spans: `retrieve`, `rerank`, `generate`, `tool`, `policy`.

This is intentionally minimal so you can pipe it to your own observability stack later.
