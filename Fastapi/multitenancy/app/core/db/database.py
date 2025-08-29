# app/core/db/database.py
from contextlib import contextmanager
from typing import Optional
from fastapi import Depends, Request
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from .settings import settings
from app.core.models import get_shared_metadata
from app.core.helper.errors import TenantNotFoundError

engine: Engine = create_engine(settings.DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def with_db(tenant_schema: Optional[str]):
    connectable = (
        engine.execution_options(schema_translate_map={"tenant": tenant_schema})
        if tenant_schema
        else engine
    )
    db = Session(bind=connectable, autoflush=False, autocommit=False)
    try:
        yield db
    finally:
        db.close()


def init_shared_db() -> None:
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS shared"))
        get_shared_metadata().create_all(bind=conn)


def _lookup_tenant_schema(db: Session, host: str) -> str:
    """
    Resolve tenant by Host header. Tries exact host:port first, then hostname.
    """
    from app.core.models import Tenant

    raw = host.strip()
    host_only = raw.split(":", 1)[0]

    # Try exact match (host:port), then fallback to hostname-only
    tenant = (
        db.query(Tenant).filter(Tenant.host.ilike(raw)).one_or_none()
        or db.query(Tenant).filter(Tenant.host.ilike(host_only)).one_or_none()
    )

    if tenant is None:
        raise TenantNotFoundError(f"No tenant for host={host}")
    return tenant.schema


# ✅ Dependency: Request is injected by FastAPI
def get_tenant(request: Request) -> str:
    host = request.headers.get("host", "")
    with with_db(None) as db:
        return _lookup_tenant_schema(db, host)


# ✅ Dependency: tenant_schema is injected via Depends(get_tenant)
def get_db(tenant_schema: str = Depends(get_tenant)):
    with with_db(tenant_schema) as db:
        yield db


def create_tenant_tables(schema: str) -> None:
    """
    Create all tenant-scoped tables inside the given schema using a
    connection that carries schema_translate_map. This avoids losing
    execution options via Session.connection().
    """
    from app.core.models import get_tenant_metadata  # ensures models imported

    connectable = engine.execution_options(schema_translate_map={"tenant": schema})
    with connectable.begin() as conn:
        get_tenant_metadata().create_all(bind=conn)
