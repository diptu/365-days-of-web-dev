# app/tests/unit/test_db_ping_direct.py
import asyncio
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings


@pytest.mark.asyncio
async def test_direct_select_one() -> None:
    # Create a throwaway engine just for this test
    tmp_engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        connect_args={"ssl": settings.ASYNCPG_SSL},
    )
    try:
        async with tmp_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar_one() == 1
    finally:
        # Dispose the temporary engine and give the loop a tick
        await tmp_engine.dispose()
        await asyncio.sleep(0)  # let asyncpg finish any pending cancellations
