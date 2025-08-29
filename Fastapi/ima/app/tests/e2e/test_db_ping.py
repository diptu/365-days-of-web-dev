import pytest
import httpx
from app import app


@pytest.mark.asyncio
async def test_db_ping(monkeypatch):
    # If DB isn’t running, this will fail — that’s expected.
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/v1/db-ping")
        assert r.status_code == 200
        assert r.json() == {"db": True}
