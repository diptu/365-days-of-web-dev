from pydantic import BaseModel, EmailStr
from typing import Optional


class StudentBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class StudentCreate(StudentBase):
    full_name: str
    email: EmailStr


class StudentUpdate(StudentBase):
    pass


class StudentOut(StudentBase):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True
