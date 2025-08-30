# app/tests/integration/test_members_post_and_list.py
import httpx
import pytest
from uuid import uuid4
import subprocess, sys

from app import app
from app.core.db.session import AsyncSessionLocal
from app.core.db.tenancy import slug_to_schema
from app.tests.utils.ensure_tenant_tables import ensure_tenant_tables


def _upgrade_head() -> None:
    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)


@pytest.mark.asyncio
async def test_create_member_and_list_in_tenant():
    slug = f"acme-{uuid4().hex[:8]}"
    # create org (creates tenant schema)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        r = await client.post("/v1/orgs", json={"name": "Acme", "slug": slug})
        assert r.status_code == 201

    # migrate new schema to head (and ensure tables exist defensively)
    _upgrade_head()
    schema = slug_to_schema(slug)
    async with AsyncSessionLocal() as s:
        await ensure_tenant_tables(s, schema)

    # create member via API
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
        headers={"X-Org-ID": slug},
    ) as client:
        c = await client.post(
            "/v1/members", json={"email": "alice@acme.com", "full_name": "Alice"}
        )
        assert c.status_code == 201
        created = c.json()
        assert created["email"] == "alice@acme.com"

        # list should include the new member
        g = await client.get("/v1/members")
        assert g.status_code == 200
        lst = g.json()
        assert any(m["email"] == "alice@acme.com" for m in lst)
