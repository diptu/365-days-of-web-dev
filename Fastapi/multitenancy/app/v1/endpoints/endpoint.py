# app/v1/endpoints/endpoint.py
from fastapi import FastAPI, APIRouter, Request
from app.v1.api import api_router
from app.core.db.database import init_shared_db
from app.core.helper.response import http_exception_handler
from app.core.helper.errors import TenantNotFoundError

app = FastAPI(title="Fast-multitenecy")

init_shared_db()  # create shared schema/tables if missing
app.include_router(api_router, prefix="/api")

app.add_exception_handler(TenantNotFoundError, http_exception_handler)

ping_router = APIRouter(tags=["health"])


@ping_router.get("/")
def ping():
    return {"status": "ok"}


@ping_router.get("/host")
def root(request: Request):
    return {"Host": request.headers["host"]}


app.include_router(ping_router, prefix="/ping")
