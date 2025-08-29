from typing import Optional
from sqlmodel import SQLModel, Field
import uuid


class User(SQLModel, table=True):
    __tablename__ = "user"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: Optional[str] = None
    is_active: bool = True
