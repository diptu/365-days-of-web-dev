from fastapi import FastAPI

from app.core.routes.student import router as StudentRouter

from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.db.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    s = get_settings()
    client = AsyncIOMotorClient(
        s.MONGO_URI, serverSelectionTimeoutMS=10_000, appname=s.APP_NAME
    )
    app.state.db = client[s.MONGO_DB]
    try:
        # Fail fast if cluster unreachable
        await app.state.db.command("ping")
        yield
    finally:
        client.close(lifespan=lifespan)


app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
