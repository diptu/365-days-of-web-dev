from fastapi import FastAPI
from app.routers.tenant import router as tenant_router
from app.database import engine

from app.tenant_a.models import Base as TenantABase
from app.tenant_b.models import Base as TenantBBase

# Create tables for known tenants (you can do this per-tenant on demand too)
TenantABase.metadata.create_all(bind=engine)
TenantBBase.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Multitenancy (schemas)")
app.include_router(tenant_router)
