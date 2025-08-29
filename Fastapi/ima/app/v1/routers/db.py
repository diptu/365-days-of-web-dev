from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_session

router = APIRouter()


@router.get("/db-ping")
async def db_ping(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))
    return {"db": result.scalar() == 1}
