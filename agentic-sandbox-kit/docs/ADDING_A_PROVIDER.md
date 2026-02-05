# Adding an LLM provider

The kit ships with `MockLLM` so everything works offline.

To add a real provider:
1. Implement `Provider.generate(messages, tools, config) -> str`
2. Return an **action JSON** string:
   - tool call: `{"type":"tool","name":"calc","args":{"expression":"2+2"}}`
   - final: `{"type":"final","content":"..."}`
3. Wire it in `providers/factory.py`

Keep providers thin. Put safety checks in the sandbox layer.
