# app/db.py
from __future__ import annotations

import os
import re
from typing import Any

from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session, sessionmaker

from .tenancy.context import get_current_tenant

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "multi_tenancy")

# Prefer psycopg3 driver; switch to +psycopg2 if you’re on psycopg2.
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# Allow only safe Postgres identifier characters for schema names.
_TENANT_RE = re.compile(r"^[a-z_][a-z0-9_]{0,62}$")


@event.listens_for(SessionLocal, "after_begin")
def _set_search_path(
    session: Session,  # noqa: ARG001 - required by SQLAlchemy hook
    transaction: Any,  # noqa: ANN401 - SQLAlchemy provides opaque type here
    connection: Connection,
) -> None:
    tenant = (get_current_tenant() or "public").strip().lower()
    tenant = tenant if _TENANT_RE.fullmatch(tenant) else "public"
    # SET LOCAL keeps it scoped to the current transaction only.
    connection.exec_driver_sql(f'SET LOCAL search_path TO "{tenant}", public')
