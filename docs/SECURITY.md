# `vulnerable` branch — intentional weaknesses

**You are on the `vulnerable` branch.** This code is for **localhost exploitation practice** only.

| OWASP category | Location | Issue |
|----------------|----------|--------|
| A03 Injection | `/search` | SQL built with f-string from user input |
| A03 Injection | `/greeting` | Reflected XSS via Jinja2 `safe` filter |
| A05 Misconfiguration | `app.py` | `DEBUG = True` |

**Patched baseline:** `git checkout main` and read `docs/SECURITY.md` there.

**Compare branches:** `git diff main..vulnerable`
