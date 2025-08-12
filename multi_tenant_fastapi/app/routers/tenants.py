from fastapi import APIRouter, status
from ..tenancy.service import create_tenant

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("/{name}", status_code=status.HTTP_201_CREATED)
def create_tenant_api(name: str):
    create_tenant(name)
    return {"ok": True, "tenant": name}
