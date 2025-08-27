# app/tenancy/service.py
from __future__ import annotations

import re
from ..db import engine
from ..models.base import Base
from ..models import shared  # noqa: F401  (register tables on metadata)

_TENANT_RE = re.compile(r"^[a-z_][a-z0-9_]{0,62}$")  # Postgres identifier rules-ish


def _sanitize_tenant(name: str | None) -> str:
    """
    Normalize and validate a tenant (schema) name.

    - lowercases
    - trims whitespace
    - allows only [a-z0-9_], must start with [a-z_]
    - max length ~63 (common PG identifier limit)
    """
    if not name:
        raise ValueError("Empty tenant name")
    safe = name.strip().lower()
    if not _TENANT_RE.fullmatch(safe):
        raise ValueError(
            "Invalid tenant name. Use letters, numbers, and underscores; "
            "must start with a letter or underscore."
        )
    return safe


def create_tenant(tenant: str) -> None:
    """
    Create a schema if it doesn't exist, switch search_path for the txn,
    and create tables for that schema.
    """
    safe = _sanitize_tenant(tenant)

    # Use a transaction. SET LOCAL limits search_path to this txn only.
    with engine.begin() as conn:  # type: Connection
        conn.exec_driver_sql(f'CREATE SCHEMA IF NOT EXISTS "{safe}"')
        conn.exec_driver_sql(f'SET LOCAL search_path TO "{safe}", public')
        Base.metadata.create_all(bind=conn)
