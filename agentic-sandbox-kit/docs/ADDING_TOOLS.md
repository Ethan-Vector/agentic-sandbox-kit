# Adding tools

Tools are regular Python callables wrapped in a `Tool` object.

## Rules (non-negotiable)
1. **No shell execution**. If you need it, you're building a different product.
2. **Constrain IO** to `workspace/` unless you have a very good reason.
3. **Validate args** and fail fast with clear errors.
4. **Make it testable**: deterministic output, no randomness in CI.

## Steps
1. Add a new tool file under `src/agentic_sandbox_kit/tools/`.
2. Register it in `src/agentic_sandbox_kit/tools/__init__.py`.
3. Add unit tests in `tests/test_tools_*.py`.
4. Add it to `configs/config.example.json` allowlist if needed.

## Tool signature
A tool receives `(args: dict, ctx: ToolContext) -> ToolResult`.

- `ctx.workspace` gives you a safe filesystem root
- `ctx.deadline` lets you respect timeouts
