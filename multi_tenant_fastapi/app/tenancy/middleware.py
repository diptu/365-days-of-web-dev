from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .context import set_current_tenant


def _tenant_from_host(host: str, root_domain: str | None) -> str | None:
    if not host:
        return None
    host = host.split(":")[0]
    if root_domain and host.endswith(root_domain):
        sub = host[: -(len(root_domain))].rstrip(".")
        if sub:
            return sub.split(".")[0]
    return None


class TenantMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, root_domain: str | None = None, default: str = "public"):
        super().__init__(app)
        self.root_domain = root_domain
        self.default = default

    async def dispatch(self, request: Request, call_next):
        tenant = request.headers.get("X-Tenant")
        if not tenant:
            tenant = _tenant_from_host(
                request.headers.get("host", ""), self.root_domain
            )
        set_current_tenant(tenant or self.default)
        return await call_next(request)
