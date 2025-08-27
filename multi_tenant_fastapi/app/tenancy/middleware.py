# app/tenancy/middleware.py
from __future__ import annotations

from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp

from .context import set_current_outlet, set_current_tenant


def _parse_labels(hostname: str | None) -> list[str]:
    if not hostname:
        return []
    return hostname.lower().strip(".").split(".")


def _resolve_tenant_outlet(
    hostname: str | None, root_domain: str | None
) -> tuple[str | None, str | None]:
    """
    Returns (tenant, outlet)
    - outlet.tenant.root → ('tenant', 'outlet')
    - tenant.root       → ('tenant', None)
    """
    if not hostname or not root_domain:
        return (None, None)

    labels = _parse_labels(hostname)
    root_labels = _parse_labels(root_domain)
    if len(labels) <= len(root_labels):
        return (None, None)
    if labels[-len(root_labels) :] != root_labels:
        return (None, None)

    sublabels = labels[: -len(root_labels)]  # everything before root
    if len(sublabels) == 1:
        # tenant.root
        return (sublabels[0], None)
    # outlet.tenant.root (take the last as tenant, first as outlet)
    return (sublabels[-1], sublabels[0])


class TenantMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: ASGIApp, *, root_domain: str | None = None, default: str = "public"
    ) -> None:
        super().__init__(app)
        self.root_domain = (root_domain or "").lstrip(".").lower() or None
        self.default = default

    async def dispatch(self, request: Request, call_next: Callable):
        # Header overrides (primarily for local/dev)
        tenant = request.headers.get("x-tenant")
        outlet = request.headers.get("x-outlet")

        # From host if not provided
        if not tenant:
            host = request.url.hostname
            t, o = _resolve_tenant_outlet(host, self.root_domain)
            tenant = t or tenant
            outlet = o or outlet

        set_current_tenant(tenant or self.default)
        set_current_outlet(outlet)
        return await call_next(request)
