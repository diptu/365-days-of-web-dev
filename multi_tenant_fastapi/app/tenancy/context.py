from contextvars import ContextVar

_CURRENT_TENANT: ContextVar[str] = ContextVar("CURRENT_TENANT", default="public")


def get_current_tenant() -> str:
    return _CURRENT_TENANT.get()


def set_current_tenant(tenant: str | None) -> None:
    tenant = (tenant or "public").strip().replace('"', "")
    _CURRENT_TENANT.set(tenant or "public")
