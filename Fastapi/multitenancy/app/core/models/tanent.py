import sqlalchemy as sa
from .base import Base


# Shared model: lives in 'shared' schema
class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = ({"schema": "shared"},)

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name = sa.Column(sa.String(256), nullable=False, unique=True, index=True)
    schema = sa.Column(sa.String(256), nullable=False, unique=True)
    host = sa.Column(sa.String(256), nullable=False, unique=True)
