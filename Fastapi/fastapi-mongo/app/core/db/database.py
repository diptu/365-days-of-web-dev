from typing import Optional
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

from app.core.db.settings import get_settings

_settings = get_settings()

# Lazy, module-level singleton client
_client: Optional[AsyncIOMotorClient] = None


def _get_client() -> AsyncIOMotorClient:
    """
    Return a process-wide Mongo client (lazy init). This avoids reconnecting
    on every import and keeps a single pool per process.
    """
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(
            _settings.MONGO_URI,
            serverSelectionTimeoutMS=10_000,
            appname=_settings.APP_NAME,
        )
    return _client


def get_db() -> AsyncIOMotorDatabase:
    """Return the configured database handle."""
    return _get_client()[_settings.MONGO_DB]


def get_collection(name: str) -> AsyncIOMotorCollection:
    """Return a collection by name (no need to list them in settings)."""
    return get_db()[name]
