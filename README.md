# Vulnerable Flask App — AppSec Learning Project

A deliberately insecure Python Flask web application built for learning Application Security. The **`main`** branch is the **patched, localhost-safe** baseline; the **`vulnerable`** branch keeps exploitable patterns for hands-on practice.

## Purpose

- Reproduce OWASP-style issues (injection, XSS, misconfiguration) in a small codebase
- Document findings and fixes in a concise security note (`docs/SECURITY.md`)
- Mirror part of an AppSec workflow: reproduce → understand fix → regression test

## Tech stack

- Python 3
- Flask
- SQLite
- Jinja2
- pytest (dev)

## Project structure

```
vulnerable-flask-app/
├── app.py                 # Flask app + routes
├── requirements.txt       # Pinned runtime deps
├── requirements-dev.txt     # pytest (optional)
├── app.db                 # SQLite (created on first run, gitignored)
├── docs/
│   └── SECURITY.md        # Posture + findings table (main)
├── templates/
│   ├── index.html
│   ├── search.html
│   └── greeting.html
├── tests/
│   ├── conftest.py        # Test client + isolated DB
│   └── test_app.py
├── static/                # Reserved for future XSS/static labs
└── .gitignore
```

**Why this layout:** One `app.py` keeps every route visible for study; `docs/SECURITY.md` is the “report appendix” without cluttering code; tests lock in the patched behavior on `main`.

## Setup

```bash
python3 -m venv .venv
source .venv/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

### Local development with debug

Debug mode is **off** by default on `main`. To enable Flask’s debugger while you iterate (localhost only):

```bash
export FLASK_DEBUG=true
python app.py
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Branches

| Branch | Purpose |
|--------|---------|
| **`main`** | Patched defaults: parameterized SQL, escaped greeting, debug gated by `FLASK_DEBUG` |
| **`vulnerable`** | Intentionally weak patterns for exploitation (SQLi string concat, XSS via Jinja2 `safe` filter, debug on) |

Checkout the lab branch:

```bash
git checkout vulnerable
```

Return to the safe baseline:

```bash
git checkout main
```

## Phase 2

Line-by-line audit, threat modeling, and vocabulary live in a separate session. Start from `docs/SECURITY.md` and `git diff main..vulnerable`.
