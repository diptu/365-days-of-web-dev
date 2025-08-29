import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData


# All tenant-scoped tables default to placeholder schema 'tenant'
# (remapped at runtime via schema_translate_map).
metadata = MetaData(schema="tenant")
Base = declarative_base(metadata=metadata)


def get_shared_metadata() -> sa.MetaData:
    """
    Collects tables that are *not* in the tenant schema (e.g., 'shared').
    """
    meta = sa.MetaData()
    for table in Base.metadata.tables.values():
        if table.schema != "tenant":
            table.tometadata(meta)
    return meta


def get_tenant_metadata() -> sa.MetaData:
    """
    Collects tables that live in the tenant schema (default = 'tenant').
    """
    meta = sa.MetaData(schema="tenant")
    for table in Base.metadata.tables.values():
        if table.schema == "tenant":
            table.tometadata(meta)
    return meta
