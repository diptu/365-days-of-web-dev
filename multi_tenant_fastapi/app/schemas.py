from datetime import datetime
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


class ProductOut(ProductCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # pydantic v2: ORM mode
