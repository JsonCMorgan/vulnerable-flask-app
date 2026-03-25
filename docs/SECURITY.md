# Security posture — `main` branch

**Scope:** Local Flask + SQLite demo app for AppSec learning. Not intended for production deployment.

## Summary

| OWASP category | Location | Issue (lab) | Status on `main` |
|----------------|----------|-------------|-------------------|
| A03 Injection | `/search` | SQL injection via string-built query | **Fixed** — parameterized `?` query |
| A03 Injection | `/greeting` | Reflected XSS if template uses `\|safe` | **Fixed** — default Jinja2 escaping (no `\|safe`) |
| A05 Misconfiguration | `app.py` | Debug mode exposes stack traces / dev tools | **Mitigated** — `DEBUG` only if `FLASK_DEBUG` is set truthy |

## Design notes

- **Passwords in UI:** Search results show plaintext passwords from the seed DB. That is intentional **insecure data design** for the lab (not a secure pattern). Phase 2 can treat this as “sensitive data exposure” in a report narrative.
- **`vulnerable` branch:** Keeps exploitable variants of the above for hands-on practice. Use only on localhost.

## Phase 2 audit hints

- Trace every `request.args` / form field into SQL and HTML.
- Compare `main` vs `vulnerable` with `git diff main..vulnerable`.
