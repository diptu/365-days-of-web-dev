# app/core/db/engine.py
from __future__ import annotations

import ssl
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def _normalize_asyncpg_url(raw: str) -> tuple[str, dict]:
    """
    Ensure DSN uses asyncpg and remove params that break asyncpg (e.g. sslmode, channel_binding).
    Also provide an SSLContext via connect_args so TLS works on Neon/hosted PG.
    """
    # Trim accidental surrounding quotes from .env (e.g., 'postgresql+asyncpg://...')
    dsn = raw.strip().strip("'").strip('"')

    # Force async driver
    if dsn.startswith("postgresql://"):
        dsn = dsn.replace("postgresql://", "postgresql+asyncpg://", 1)

    parts = urlsplit(dsn)
    qs = dict(parse_qsl(parts.query, keep_blank_values=True))

    # Remove params asyncpg either doesn't accept or we don't want in the DSN
    qs.pop("sslmode", None)
    qs.pop("channel_binding", None)

    # Ensure TLS on hosted PG
    qs.setdefault("ssl", "true")

    clean = urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode(qs), parts.fragment)
    )

    # Provide a real SSLContext to asyncpg (works across providers)
    ssl_ctx = ssl.create_default_context()
    connect_args = {"ssl": ssl_ctx}

    return clean, connect_args


_clean_url, _connect_args = _normalize_asyncpg_url(settings.database_url)

engine = create_async_engine(
    _clean_url,
    connect_args=_connect_args,
    pool_pre_ping=True,
    echo=settings.debug,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
