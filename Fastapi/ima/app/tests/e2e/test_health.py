import pytest
import httpx
from app import app


@pytest.mark.asyncio
async def test_health():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/v1/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}
