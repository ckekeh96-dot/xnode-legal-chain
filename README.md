# XNode LegalChain AI v24 — Incremental Security Hardening

Adds a locally hash-linked audit event chain and CEO verification endpoint, plus an **optional CSRF enforcement mode**. New login responses include a CSRF token and the UI sends it for authenticated state-changing requests. Set `XNODE_ENFORCE_CSRF=1` to enable enforcement; this is **not enabled by default** for backwards compatibility with existing API clients and tests. Production would require comprehensive authentication, browser-origin review, MFA, encrypted data and independent security assessment.

Audit chaining covers **new audit events only** and checks the corresponding legacy audit rows; older records are not backfilled. A database administrator can rewrite the chain, so this is not an immutable audit log. No encryption-at-rest or MFA is implemented in this version.

## Windows 11
```
python -m pip install -r requirements.txt
$env:XNODE_ENFORCE_CSRF="1"
python -m uvicorn app:app --host 127.0.0.1 --port 8787
```
Open http://127.0.0.1:8787. Demo users `demo1`–`demo14` / `DemoOnly!2026`. Tests: `python -m pip install pytest httpx` then `python -m pytest tests -q`.

**SYNTHETIC DATA ONLY.** No live Base Sepolia tests, wallet integration, real client identities or verified electronic signatures. Not suitable for confidential legal records or trust accounting.
