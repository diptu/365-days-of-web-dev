from pydantic import BaseModel, Field
from .common import CreatedAt


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    body: str | None = None


class NoteOut(CreatedAt):
    id: int
    title: str
    body: str | None = None

    class Config:
        from_attributes = True  # SQLAlchemy -> Pydantic
