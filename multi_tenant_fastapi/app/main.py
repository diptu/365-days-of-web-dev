# app/main.py
from __future__ import annotations

import os
from fastapi import FastAPI
from dotenv import load_dotenv  # <-- add

from .tenancy.middleware import TenantMiddleware
from .tenancy.service import create_tenant
from .routers import tenants, users, notes, outlets

load_dotenv()  # <-- add this line so ROOT_DOMAIN is read

ROOT_DOMAIN = os.getenv("ROOT_DOMAIN")
DEFAULT_TENANT = os.getenv("TENANT_DEFAULT", "public")

app = FastAPI(title="Multi-tenant FastAPI (schema-per-tenant + outlets)")

app.add_middleware(
    TenantMiddleware,
    root_domain=ROOT_DOMAIN,
    default=DEFAULT_TENANT,
)


@app.on_event("startup")
def init_default_tenant() -> None:
    create_tenant(DEFAULT_TENANT)


app.include_router(tenants.router)
app.include_router(outlets.router)
app.include_router(users.router)
app.include_router(notes.router)


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok"}
