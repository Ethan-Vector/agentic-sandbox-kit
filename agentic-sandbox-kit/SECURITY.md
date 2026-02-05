# Security

This repository is designed to be **offline-first** and safe-by-default.

## Threat model (baseline)
- tools may be abused to read/write unintended files
- prompt injection may attempt to escape tool allowlists
- excessive tool loops can burn budget

## Controls shipped here
- tool allowlist enforced in the sandbox
- per-run step cap and wall-time budget
- workspace isolation under `workspace/`
- file tools are constrained to workspace by default

## If you add networked tools
- implement domain allowlists
- add SSRF protections
- add request timeouts and size caps
- log every request and response metadata

Report issues privately if possible.
