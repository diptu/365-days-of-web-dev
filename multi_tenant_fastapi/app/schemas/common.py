from datetime import datetime
from pydantic import BaseModel, Field


class Paging(BaseModel):
    limit: int = Field(ge=1, le=100, default=20)
    offset: int = Field(ge=0, default=0)


class CreatedAt(BaseModel):
    created_at: datetime
