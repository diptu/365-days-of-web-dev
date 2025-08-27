# app/tenancy/context.py
from __future__ import annotations

from contextvars import ContextVar

_CURRENT_TENANT: ContextVar[str] = ContextVar("CURRENT_TENANT", default="public")
_CURRENT_OUTLET: ContextVar[str | None] = ContextVar("CURRENT_OUTLET", default=None)


def get_current_tenant() -> str:
    return _CURRENT_TENANT.get()


def set_current_tenant(tenant: str | None) -> None:
    tenant = (tenant or "public").strip().replace('"', "").replace(";", "")
    _CURRENT_TENANT.set(tenant or "public")


def get_current_outlet() -> str | None:
    return _CURRENT_OUTLET.get()


def set_current_outlet(outlet: str | None) -> None:
    if outlet:
        outlet = outlet.strip().replace('"', "").replace(";", "")
    _CURRENT_OUTLET.set(outlet or None)
