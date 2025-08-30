# app/tests/integration/test_tenant_members_isolation.py
import httpx
import pytest
from uuid import uuid4
import subprocess, sys

from sqlalchemy.ext.asyncio import AsyncSession

from app import app
from app.core.db.session import AsyncSessionLocal
from app.core.db.tenancy import slug_to_schema, set_search_path
from app.domain.tenants.repo import create_org_user
from app.domain.tenants.models import Membership
from app.tests.utils.ensure_tenant_tables import ensure_tenant_tables  # ✅


def _upgrade_head() -> None:
    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)


@pytest.mark.asyncio
async def test_members_list_is_isolated_between_tenants():
    slug_a = f"acme-{uuid4().hex[:8]}"
    slug_b = f"beta-{uuid4().hex[:8]}"

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        r1 = await client.post("/v1/orgs", json={"name": "Acme", "slug": slug_a})
        assert r1.status_code == 201
        r2 = await client.post("/v1/orgs", json={"name": "Beta", "slug": slug_b})
        assert r2.status_code == 201

    # migrate new schemas to head
    _upgrade_head()

    schema_a = slug_to_schema(slug_a)
    schema_b = slug_to_schema(slug_b)

    # ✅ ensure tables exist in both tenants
    async with AsyncSessionLocal() as s:
        await ensure_tenant_tables(s, schema_a)
    async with AsyncSessionLocal() as s:
        await ensure_tenant_tables(s, schema_b)

    # now safe to insert members in each tenant
    async with AsyncSessionLocal() as s1:
        await set_search_path(s1, schema_a)
        u1 = await create_org_user(s1, email=f"alice@{slug_a}.com", full_name="Alice")
        s1.add(Membership(user_id=u1.id))
        await s1.commit()

    async with AsyncSessionLocal() as s2:
        await set_search_path(s2, schema_b)
        u2 = await create_org_user(s2, email=f"bob@{slug_b}.com", full_name="Bob")
        s2.add(Membership(user_id=u2.id))
        await s2.commit()

    # verify isolation via API (unchanged)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
        headers={"X-Org-ID": slug_a},
    ) as client:
        ra = await client.get("/v1/members")
        assert ra.status_code == 200
        assert any(m["email"].startswith("alice@") for m in ra.json())

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
        headers={"X-Org-ID": slug_b},
    ) as client:
        rb = await client.get("/v1/members")
        assert rb.status_code == 200
        assert any(m["email"].startswith("bob@") for m in rb.json())
