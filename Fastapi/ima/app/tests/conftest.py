# app/tests/conftest.py
import os

os.environ.setdefault("IMA_TESTING", "true")

import pytest
import subprocess, pytest

# app/tests/conftest.py  (append)
import asyncio
import pytest
from sqlalchemy import text
from app.core.db.session import AsyncSessionLocal


@pytest.fixture(autouse=True)
async def _cleanup_tenant_schemas():
    # run test
    yield
    # cleanup: drop all schemas starting with tenant_acme-/tenant_beta- test prefixes
    async with AsyncSessionLocal() as s:
        await s.execute(
            text("""
            DO $$
            DECLARE r record;
            BEGIN
              FOR r IN (SELECT nspname FROM pg_namespace WHERE nspname LIKE 'tenant_acme-%' OR nspname LIKE 'tenant_beta-%')
              LOOP
                EXECUTE format('DROP SCHEMA IF EXISTS %I CASCADE', r.nspname);
              END LOOP;
            END$$;
        """)
        )
        await s.commit()


@pytest.fixture(scope="session", autouse=True)
def _apply_migrations() -> None:
    subprocess.run(["alembic", "upgrade", "head"], check=True)


@pytest.fixture(scope="session", autouse=True)
async def _dispose_engine_on_session_end():
    yield
    from app.core.db.engine import engine

    await engine.dispose()
