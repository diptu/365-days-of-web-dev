import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.schema import CreateSchema

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "mt")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_schema_if_not_exists(schema_name: str) -> None:
    # CREATE SCHEMA IF NOT EXISTS <schema>
    with engine.connect() as conn:
        conn.execute(CreateSchema(schema_name, if_not_exists=True))
        conn.commit()


def get_base(tenant_name: str):
    """Return a declarative base bound to a tenant schema."""
    create_schema_if_not_exists(tenant_name)
    metadata = MetaData(schema=tenant_name)
    return declarative_base(metadata=metadata)
