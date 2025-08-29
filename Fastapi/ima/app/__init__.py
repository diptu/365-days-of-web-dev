from fastapi import FastAPI
from app.v1 import api
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.http.middleware import OrgContextMiddleware


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title=settings.app_name)
    app.add_middleware(OrgContextMiddleware)
    app.include_router(api)
    return app


app = create_app()
