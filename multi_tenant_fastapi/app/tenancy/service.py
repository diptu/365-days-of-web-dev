from sqlalchemy.engine import Connection
from ..db import engine
from ..models.base import Base
from ..models import shared  # noqa: F401  (register tables on metadata)


def create_tenant(tenant: str) -> None:
    safe = (tenant or "").strip().replace('"', "")
    if not safe:
        raise ValueError("Empty tenant name")

    with engine.begin() as conn:  # type: Connection
        conn.exec_driver_sql(f'CREATE SCHEMA IF NOT EXISTS "{safe}"')
        conn.exec_driver_sql(f'SET search_path TO "{safe}", public')
        Base.metadata.create_all(bind=conn)
