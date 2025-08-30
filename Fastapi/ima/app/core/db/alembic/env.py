# app/core/db/alembic/env.py
from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings
from app.core.db.base import Base
import app.core.db.models_registry  # noqa: F401  # ensure models are imported
from app.core.db.tenancy.names import is_tenant_schema

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _set_sqlalchemy_url_from_settings() -> None:
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def _include_object_for_schema(schema_name: str | None):
    """
    Return an include_object callback that:
      - Skips tenant tables when migrating public (schema_name is None)
      - Includes everything for tenant schemas
    """

    def include_object(object, name, type_, reflected, compare_to):
        if type_ == "table":
            is_tenant = getattr(getattr(object, "info", {}), "get", lambda *_: False)(
                "tenant"
            )
            if is_tenant and schema_name is None:
                return False
        return True

    return include_object


def run_migrations_offline() -> None:
    _set_sqlalchemy_url_from_settings()
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        render_as_batch=False,
        include_schemas=False,
        include_object=_include_object_for_schema(schema_name=None),
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection, schema_name: str | None = None) -> None:
    opts = dict(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        render_as_batch=False,
        include_schemas=False,  # use search_path not schema qualifiers
        include_object=_include_object_for_schema(schema_name),
    )
    if schema_name:
        # set per-tenant version table and target the tenant schema via search_path
        opts.update(
            version_table="alembic_version",
            version_table_schema=schema_name,
        )
        connection.exec_driver_sql(f'SET search_path TO "{schema_name}", public')

    context.configure(**opts)
    with context.begin_transaction():
        context.run_migrations()


async def _get_tenant_schemas(conn) -> list[str]:
    result = await conn.execute(
        text("SELECT nspname FROM pg_namespace WHERE nspname LIKE 'tenant_%'")
    )
    return [row[0] for row in result.fetchall() if is_tenant_schema(row[0])]


async def run_migrations_online() -> None:
    _set_sqlalchemy_url_from_settings()
    engine: AsyncEngine = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
        connect_args={"ssl": settings.ASYNCPG_SSL},
    )
    async with engine.connect() as connection:
        # public pass (skips tenant tables)
        await connection.run_sync(do_run_migrations, schema_name=None)

        # then each tenant (includes tenant tables)
        tenant_schemas = await _get_tenant_schemas(connection)
        for schema_name in tenant_schemas:
            await connection.run_sync(do_run_migrations, schema_name=schema_name)
    await engine.dispose()


def run() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


run()
