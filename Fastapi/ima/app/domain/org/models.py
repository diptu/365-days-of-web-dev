from sqlmodel import SQLModel, Field
import uuid


class Organization(SQLModel, table=True):
    __tablename__ = "organization"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    slug: str = Field(index=True, unique=True)
    status: str = "active"
