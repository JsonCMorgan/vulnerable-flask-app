"""
Vulnerable Flask App — AppSec Learning Project
Deliberately insecure for security audit practice.
"""
import sqlite3
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)

# Security misconfiguration (A05): debug mode ON — we'll exploit this in Phase 2
app.config["DEBUG"] = True

DB_PATH = Path(__file__).parent / "app.db"


def init_db():
    """Create the database and seed test data."""
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
    """Home page."""
    return render_template("index.html")


# --- ROUTE 2: Search (PATCHED — SQL Injection fixed) ---
@app.route("/search")
def search():
    """
    Search users by username.
    PATCHED: Uses parameterized query (? placeholder) — input is passed as data, not concatenated.
    """
    query = request.args.get("q", "")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return dict-like rows

    # SAFE: Parameterized query — ? is a placeholder; value passed separately as a tuple
    # The database treats the value as DATA only, never as SQL syntax
    sql = "SELECT * FROM users WHERE username LIKE ?"
    cursor = conn.execute(sql, (f"%{query}%",))
    results = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return render_template("search.html", query=query, results=results)


# --- Startup ---
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
