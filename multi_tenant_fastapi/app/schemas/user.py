from pydantic import BaseModel, EmailStr
from .common import CreatedAt


class UserCreate(BaseModel):
    email: EmailStr


class UserOut(CreatedAt):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
