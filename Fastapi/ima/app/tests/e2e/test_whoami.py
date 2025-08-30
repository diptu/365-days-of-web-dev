# app/tests/e2e/test_whoami.py
import httpx
import pytest

from app import app


@pytest.mark.asyncio
async def test_whoami_without_org_header():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        res = await client.get("/v1/whoami")
        assert res.status_code == 200
        assert res.json() == {"org_id": None}


@pytest.mark.asyncio
async def test_whoami_with_org_header():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
        headers={"X-Org-ID": "tenant_a"},
    ) as client:
        res = await client.get("/v1/whoami")
        assert res.status_code == 200
        assert res.json() == {"org_id": "tenant_a"}
