# app/tests/unit/test_config.py
import importlib


def _reload_settings(monkeypatch, db_url: str):
    # simulate different .env by setting env vars
    monkeypatch.setenv("IMA_DATABASE_URL", db_url)
    # optional noise params that should be ignored by asyncpg
    monkeypatch.setenv("IMA_APP_NAME", "IMA")
    monkeypatch.setenv("IMA_DEBUG", "true")
    # reload module to recompute validators
    mod = importlib.import_module("app.core.config")
    importlib.reload(mod)
    return mod.settings


def test_db_url_normalizes_to_asyncpg_remote(monkeypatch):
    s = _reload_settings(
        monkeypatch,
        "postgresql://user:pass@remote-host.example.com:5432/db"
        "?sslmode=require&channel_binding=require",
    )
    assert s.DATABASE_URL.startswith("postgresql+asyncpg://")
    # libpq-only params removed
    assert "sslmode=" not in s.DATABASE_URL
    assert "channel_binding=" not in s.DATABASE_URL
    # remote → ssl True
    assert s.ASYNCPG_SSL is True


def test_db_url_local_disables_ssl(monkeypatch):
    s = _reload_settings(
        monkeypatch,
        "postgresql://user:pass@localhost:5432/db?sslmode=require",
    )
    assert s.DATABASE_URL.startswith("postgresql+asyncpg://")
    assert "sslmode=" not in s.DATABASE_URL
    assert s.ASYNCPG_SSL is False
