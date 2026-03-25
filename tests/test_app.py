"""
Smoke + regression tests for the patched `main` branch behavior.
"""
from urllib.parse import quote


def test_index_ok(client):
    """Home route should return 200 and mention the lab."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Vulnerable App" in resp.data


def test_search_parameterized_no_error(client):
    """Search with a normal substring should return 200 (parameterized query)."""
    resp = client.get("/search?q=alice")
    assert resp.status_code == 200
    assert b"alice" in resp.data.lower()


def test_greeting_escapes_script_tag(client):
    """
    Reflected name must not render raw HTML — script should be escaped in the body.

    If we removed default escaping or added |safe in the template, this test would fail.
    """
    payload = "<script>alert(1)</script>"
    resp = client.get("/greeting?name=" + quote(payload))
    assert resp.status_code == 200
    assert b"<script>" not in resp.data
    assert b"&lt;script&gt;" in resp.data
