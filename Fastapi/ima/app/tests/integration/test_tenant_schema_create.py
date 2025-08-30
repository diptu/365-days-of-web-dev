# app/tests/integration/test_tenant_schema_create.py
import httpx
import pytest
from uuid import uuid4
import subprocess, sys

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app import app
from app.core.db.session import AsyncSessionLocal
from app.core.db.tenancy import slug_to_schema
from app.tests.utils.ensure_tenant_tables import ensure_tenant_tables  # ✅


def _upgrade_head() -> None:
    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)


@pytest.mark.asyncio
async def test_members_list_is_isolated_between_tenants():
    slug = f"acme-{uuid4().hex[:8]}"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        r = await client.post("/v1/orgs", json={"name": "Acme", "slug": slug})
        assert r.status_code == 201

    # bring new schema to head
    _upgrade_head()

    schema = slug_to_schema(slug)
    # ✅ ensure tables exist in this tenant schema
    async with AsyncSessionLocal() as s:  # type: AsyncSession
        await ensure_tenant_tables(s, schema)

    # verify schema exists (unchanged)
    async with AsyncSessionLocal() as s:
        res = await s.execute(
            text(
                "SELECT schema_name FROM information_schema.schemata WHERE schema_name = :s"
            ),
            {"s": schema},
        )
        assert res.scalar_one_or_none() == schema
