"""
Vulnerable Flask App — AppSec Learning Project
**vulnerable branch** — deliberately insecure for exploitation practice (localhost only).
"""
import sqlite3
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)

# --- Security misconfiguration (A05) ---
# VULNERABLE: debug ON — stack traces and dev tooling exposed; never ship like this.
app.config["DEBUG"] = True

DB_PATH = Path(__file__).parent / "app.db"


def init_db():
    """
    Create SQLite schema and seed fake users for the lab.

    Block job: give the search route predictable rows so SQLi demos behave the same
    every time. Never use real credentials here.
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


# --- ROUTE 2: Search (VULNERABLE — SQL Injection) ---
@app.route("/search")
def search():
    """
    Search users by username substring.

    Block job: **VULNERABLE** — user input is concatenated into SQL. Attacker-controlled
    syntax can change query meaning (A03: Injection). Compare `main` for the fix.
    """
    query = request.args.get("q", "")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # VULNERABLE: Never build SQL with string concatenation / f-strings from user input.
    sql = f"SELECT * FROM users WHERE username LIKE '%{query}%'"
    cursor = conn.execute(sql)
    results = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return render_template("search.html", query=query, results=results)


# --- ROUTE 3: Greeting (VULNERABLE — XSS) ---
@app.route("/greeting")
def greeting():
    """
    Personalized greeting from the `name` query parameter.

    Block job: **VULNERABLE** — template uses |safe so HTML/JS in `name` may execute (A03 XSS).
    """
    name = request.args.get("name", "visitor")
    return render_template("greeting.html", name=name)


# --- Startup ---
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
