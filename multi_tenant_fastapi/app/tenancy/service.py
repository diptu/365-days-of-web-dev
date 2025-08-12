from sqlalchemy.engine import Connection
from ..db import engine
from ..models.base import Base

# IMPORTANT: import models so they are registered on Base.metadata
# Without this, create_all() has no tables to create.
from ..models import shared  # noqa: F401  (side-effect import)


def create_tenant(tenant: str) -> None:
    safe = (tenant or "").strip().replace('"', "")
    if not safe:
        raise ValueError("Empty tenant name")

    with engine.begin() as conn:  # type: Connection
        conn.exec_driver_sql(f'CREATE SCHEMA IF NOT EXISTS "{safe}"')
        conn.exec_driver_sql(f'SET search_path TO "{safe}", public')
        # Now metadata knows about User/Note because of the side-effect import above
        Base.metadata.create_all(bind=conn)
