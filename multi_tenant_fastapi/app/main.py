from fastapi import FastAPI
from .tenancy.middleware import TenantMiddleware
from .routers import tenants, users, notes

app = FastAPI(title="Multi-tenant FastAPI (schema-per-tenant)")

# In dev: use the X-Tenant header; in prod, set root_domain
app.add_middleware(TenantMiddleware, root_domain=None, default="public")

# Routers
app.include_router(tenants.router)
app.include_router(users.router)
app.include_router(notes.router)
