# app/tests/integration/test_create_org.py
import httpx
import pytest
from uuid import uuid4

from app import app


@pytest.mark.asyncio
async def test_create_org_ok():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        slug = f"acme-{uuid4().hex[:8]}"
        payload = {"name": "Acme Inc", "slug": slug}
        r = await client.post("/v1/orgs", json=payload)
        assert r.status_code == 201, r.text
        data = r.json()
        assert data["name"] == "Acme Inc"
        assert data["slug"] == slug
        assert "id" in data


@pytest.mark.asyncio
async def test_create_org_conflict_slug():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        slug = f"dup-{uuid4().hex[:8]}"
        payload = {"name": "Dup Inc", "slug": slug}
        r1 = await client.post("/v1/orgs", json=payload)
        assert r1.status_code == 201, r1.text
        r2 = await client.post("/v1/orgs", json=payload)
        assert r2.status_code == 409
        assert r2.json()["detail"] == "slug_already_exists"
