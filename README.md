# ethan-agentic-sandbox-kit

Agent runtime “permissioned”: tool router + capability tokens + policy enforcement + audit events + sandboxed execution.

Obiettivo: dimostrare (per il libro) che “agentic” in produzione significa soprattutto **blast radius control**:
- **least privilege** (scope-based)
- **capability tokens** (TTL, max calls, limits)
- **policy guard boundary** (route → tools allowlist)
- **sandboxing** (filesystem + subprocess allowlist + timeout)
- **audit-grade logging** (chi ha fatto cosa, con quale permesso)

> Nota: qui non c’è un LLM. Questo kit è il **runtime sicuro** su cui puoi innestare qualsiasi planner/LLM.

---

## Quickstart

### 1) Setup
```bash
cp .env.example .env
cp configs/policies.example.yaml configs/policies.yaml

python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2) Run API
```bash
make dev
# http://localhost:8095/healthz
```

### 3) Genera un capability token
```bash
sandboxkit token --sub "alice" --scopes tool.fs.read tool.fs.write --ttl 3600
```

### 4) Esegui un tool call (API)
```bash
TOKEN="<incolla token qui>"

curl -s http://localhost:8095/v1/tools/fs.write \
  -H "content-type: application/json" \
  -H "authorization: Bearer $TOKEN" \
  -H "x-route: default" \
  -d '{"path":"notes/hello.txt","content":"ciao"}' | jq
```

### 5) Esegui security harness (prompt injection / privilege escalation)
```bash
sandboxkit security-test --config configs/policies.yaml
```

---

## Concept: Capability Tokens

Token firmato HMAC (non JWT) con payload:
- `sub` (caller identity)
- `scopes` (es. `tool.shell.exec`)
- `exp` (unix seconds)
- `limits.max_calls` (counter enforced server-side per request, demo-friendly)

---

## Policy Model

Config YAML:
- `routes.<route>.allowed_tools`: allowlist (es. `fs.read`, `shell.exec`)
- `tools.<tool>.required_scopes`: scope richiesto (es. `tool.shell.exec`)
- `sandbox`: root dir, allowlist comandi shell, timeout

Questo crea un boundary chiaro: anche se un LLM “impazzisce”, non può oltrepassare policy + token.

---

## License
MIT
