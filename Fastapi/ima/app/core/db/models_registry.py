# app/core/db/models_registry.py
"""
Import all ORM models here so Alembic autogenerate can discover them
without creating circular imports at runtime.
"""

# Global tables
from app.domain.users.models import User  # noqa: F401
from app.domain.org.models import Organization  # noqa: F401

# Tenant tables
from app.domain.tenants.models import OrgUser, Membership  # noqa: F401
