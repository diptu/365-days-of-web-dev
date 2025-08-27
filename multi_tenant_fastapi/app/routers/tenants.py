# app/routers/tenants.py
from __future__ import annotations

from fastapi import APIRouter, Path, status

from ..tenancy.service import create_tenant

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("/{name}", status_code=status.HTTP_201_CREATED)
def create_tenant_api(
    name: str = Path(..., min_length=1, max_length=100, description="Tenant name"),
) -> dict[str, str | bool]:
    """Create a new tenant by name."""
    create_tenant(name)
    return {"ok": True, "tenant": name}
