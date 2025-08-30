# app/tests/conftest.py
import os

os.environ.setdefault("IMA_TESTING", "true")

import pytest


@pytest.fixture(scope="session", autouse=True)
async def _dispose_engine_on_session_end():
    yield
    from app.core.db.engine import engine

    await engine.dispose()
