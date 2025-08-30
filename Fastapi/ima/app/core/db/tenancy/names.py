# app/core/db/tenancy/names.py
from __future__ import annotations

import re


_SCHEMA_PREFIX = "tenant_"
_VALID = re.compile(r"^[a-z0-9_]+$")


def slug_to_schema(slug: str) -> str:  # type: ignore[name-defined]
    """
    Convert an org slug to a safe schema name:
      - lowercase
      - replace '-' with '_'
      - prefix with 'tenant_'
      - enforce [a-z0-9_]+
    """
    s = str(slug).strip().lower().replace("-", "_")
    schema = f"{_SCHEMA_PREFIX}{s}"
    if not _VALID.match(schema):
        raise ValueError("invalid schema name")
    return schema


def is_tenant_schema(name: str) -> bool:
    return name.startswith(_SCHEMA_PREFIX)
