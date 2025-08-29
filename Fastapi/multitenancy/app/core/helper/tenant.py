# app/core/helper/tenant.py

from sqlalchemy import text
from app.core.db.database import with_db

# ✅ Import models so they are registered on Base.metadata
import app.core.models.student_model  # noqa: F401
import app.core.models.tenant_model  # noqa: F401

# Import after models are registered
from app.core.models import Tenant, get_tenant_metadata  # noqa: E402


def create_tenant_schema(schema: str, name: str, host: str) -> None:
    """
    Create schema + tables for a new tenant, and insert a row in shared.tenants.
    Idempotent: safe to call multiple times.
    """
    # 1) Ensure schema exists
    with with_db(None) as db:
        db.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
        db.commit()

    # 2) Create tenant tables in that schema
    with with_db(schema) as db:
        get_tenant_metadata().create_all(bind=db.connection())

    # 3) Insert tenant row (if missing)
    with with_db(None) as db:
        exists = db.query(Tenant).filter(Tenant.schema == schema).one_or_none()
        if not exists:
            tenant = Tenant(name=name, schema=schema, host=host)
            db.add(tenant)
            db.commit()
