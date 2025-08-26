import asyncio
import os
import sys
from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from app.core.config import settings  # type: ignore
from app.db.base import Base  # type: ignore
from app.models.users import User  # type: ignore

config = context.config
DB_URL = getattr(settings, "AUTH_DB_URL", None) or getattr(settings, "TEST_AUTH_DB_URL", None)
if DB_URL:
    config.set_main_option("sqlalchemy.url", DB_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

assert User.metadata is Base.metadata

target_metadata = Base.metadata
if not target_metadata.tables:
    raise RuntimeError("target_metadata.tables is empty")

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    url = config.get_main_option("sqlalchemy.url") or DB_URL
    if url and url.startswith("postgresql+asyncpg"):
        url = url.replace("postgresql+asyncpg", "postgresql+psycopg2")
    from sqlalchemy import create_engine
    connectable = create_engine(url, poolclass=pool.NullPool)  # type: ignore
    with connectable.connect() as connection:
        do_run_migrations(connection)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
