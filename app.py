"""
Vulnerable Flask App — AppSec Learning Project
Deliberately insecure for security audit practice.
"""
import os
import sqlite3
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)

# --- Security configuration (A05: Security Misconfiguration) ---
# On `main`, debug is OFF unless you explicitly opt in (local dev only).
# Phase 2: why DEBUG=True in production is dangerous (stack traces, Werkzeug PIN).
_debug = os.environ.get("FLASK_DEBUG", "").strip().lower() in ("1", "true", "yes")
app.config["DEBUG"] = _debug

DB_PATH = Path(__file__).parent / "app.db"


def init_db():
    """
    Create SQLite schema and seed fake users for the lab.

    Block job: give the search route predictable rows so SQLi / safe search demos
    behave the same every time. Never use real credentials here.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
        INSERT OR IGNORE INTO users (id, username, password) VALUES
            (1, 'admin', 'admin123'),
            (2, 'alice', 'alice456'),
            (3, 'bob', 'bob789');
    """)
    conn.commit()
    conn.close()


# --- ROUTE 1: Home ---
@app.route("/")
def index():
    """Landing page with navigation to lab routes."""
    return render_template("index.html")


# --- ROUTE 2: Search (PATCHED — SQL Injection fixed on main) ---
@app.route("/search")
def search():
    """
    Search users by username substring.

    Block job: run a read-only query and pass rows to the template. On `main` the
    query is parameterized so user input cannot change SQL structure (A03: Injection).
    """
    query = request.args.get("q", "")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # SAFE: Parameterized query — ? is a placeholder; value passed separately as a tuple.
    # The database treats the value as DATA only, never as SQL syntax.
    sql = "SELECT * FROM users WHERE username LIKE ?"
    cursor = conn.execute(sql, (f"%{query}%",))
    results = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return render_template("search.html", query=query, results=results)


# --- ROUTE 3: Greeting (PATCHED — XSS fixed on main) ---
@app.route("/greeting")
def greeting():
    """
    Personalized greeting from the `name` query parameter.

    Block job: pass untrusted text to Jinja2 with default auto-escaping (no |safe).
    See `vulnerable` branch for the unsafe |safe pattern (Phase 2).
    """
    name = request.args.get("name", "visitor")
    return render_template("greeting.html", name=name)


# --- Startup ---
if __name__ == "__main__":
    init_db()
    app.run(debug=_debug)
