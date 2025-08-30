# app/tests/e2e/test_health.py
import pytest
import httpx

from app import app


@pytest.mark.asyncio
async def test_health_ok() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        res = await client.get("/v1/health")
        assert res.status_code == 200
        assert res.json() == {"status": "ok"}
