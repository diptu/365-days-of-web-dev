import pytest
import httpx
from app import app


@pytest.mark.asyncio
async def test_whoami_ok():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/v1/whoami", headers={"X-Org-ID": "tenant_acme"})
        assert r.status_code == 200
        assert r.json() == {"org_id": "tenant_acme"}


@pytest.mark.asyncio
async def test_whoami_missing_header():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/v1/whoami")
        assert r.status_code == 400
        assert r.json()["detail"] == "Missing X-Org-ID"
