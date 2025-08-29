from typing import Any, Optional
from fastapi.responses import JSONResponse
from fastapi import Request
from .errors import TenantNotFoundError


def success_response(
    message: str = "Request successful",
    details: Optional[Any] = None,
    code: str = "SUCCESS",
    status_code: int = 200,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "code": code,
            "message": message,
            "details": details,
        },
    )


def error_response(
    message: str = "An error occurred",
    details: Optional[Any] = None,
    code: str = "ERROR",
    status_code: int = 400,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "code": code,
            "message": message,
            "details": details,
        },
    )


def http_exception_handler(request: Request, exc: TenantNotFoundError):
    return error_response(
        message="Tenant not found",
        details={"host": request.headers.get("host")},
        code="TENANT_NOT_FOUND",
        status_code=403,
    )
