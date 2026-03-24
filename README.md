# Vulnerable Flask App — AppSec Learning Project

A deliberately insecure Python Flask web application built for learning Application Security. Each vulnerability is documented, exploited, and patched with full OWASP context.

## Purpose

- Build vulnerabilities from OWASP Top 10 (SQLi, XSS, broken auth, etc.)
- Document findings in professional security report format
- Patch each flaw and explain the fix
- Mirror real AppSec analyst workflow

## Tech Stack

- Python 3
- Flask
- SQLite
- Jinja2

## Project Structure

```
vulnerable-flask-app/
├── app.py              # Main Flask application + all routes
├── requirements.txt    # Python dependencies (Flask)
├── app.db              # SQLite database (created on first run, gitignored)
├── templates/          # Jinja2 HTML templates
│   ├── index.html
│   └── search.html
├── static/             # Static assets (CSS, JS, images) — used later for XSS
└── .gitignore          # Keeps secrets, .db files, venv out of git
```

**Why each piece matters:**
- `app.py` — Single entry point. In production apps you'd split routes/models, but here we keep it flat so every vulnerability is easy to trace.
- `templates/` — Flask's default. Jinja2 renders HTML and injects variables (this is where XSS will live).
- `static/` — Served directly by Flask. No server-side processing = different attack surface than templates.
- `app.db` — SQLite file. Never commit this; it holds our fake user data.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit http://127.0.0.1:5000

## Branches

- `vulnerable` — insecure version (for exploitation practice)
- `main` (patched) — secured version with fixes documented
