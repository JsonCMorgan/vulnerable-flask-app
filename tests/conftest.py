"""
Pytest fixtures: isolate the SQLite file so tests never touch your real app.db.
"""
import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    """
    Flask test client with DB_PATH pointing at a temp database.

    Block job: import `app` after patching DB_PATH, seed rows, then hand back
    a client — same routes as production, zero side effects on disk in the project root.
    """
    import app as app_module

    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "test.db")
    app_module.init_db()
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()
