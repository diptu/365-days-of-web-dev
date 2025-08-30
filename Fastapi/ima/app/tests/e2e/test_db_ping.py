# app/tests/e2e/test_db_ping.py
import httpx
import pytest

from app import app


@pytest.mark.asyncio
async def test_db_ping_ok():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        res = await client.get("/v1/db-ping")
        assert res.status_code == 200
        assert res.json() == {"status": "ok"}
