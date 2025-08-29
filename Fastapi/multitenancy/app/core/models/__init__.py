# app/core/models/__init__.py

# Ensure models are imported so Base.metadata is populated
from . import tanent as _tenant_model  # noqa: F401
from . import student as _student_model  # noqa: F401

from .base import Base, get_shared_metadata, get_tenant_metadata
from .tanent import Tenant
from .student import Student

__all__ = [
    "Base",
    "get_shared_metadata",
    "get_tenant_metadata",
    "Tenant",
    "Student",
]
