import sqlalchemy as sa
from .base import Base


# Tenant-scoped model: defaults to 'tenant' schema (remapped per request)
class Student(Base):
    __tablename__ = "students"

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    full_name = sa.Column(sa.String(256), nullable=False, index=True)
    email = sa.Column(sa.String(256), nullable=False, unique=True, index=True)
