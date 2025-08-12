# app/tenant_resolver.py
from fastapi import Header, HTTPException, status


def get_tenant(x_tenant: str = Header(..., alias="X-Tenant")) -> str:
    t = x_tenant.strip().lower()
    if not t:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing tenant."
        )
    return t
