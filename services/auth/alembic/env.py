# # import asyncio
# # import os
# # import sys
# # from logging.config import fileConfig

# # from alembic import context
# # from sqlalchemy import pool



# # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
# # # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  "../src")))

# # from src.app.core.config import settings
# # from src.app.db.base import Base
# # from src.app.models.users import User
# # from src.app.models.teams import Team
# # from src.app.models.access_token import AccessToken


# # config = context.config

# # config.set_main_option("sqlalchemy.url", settings.TEST_AUTH_DB_URL)

# # if config.config_file_name is not None:
# #     fileConfig(config.config_file_name)


# # target_metadata = Base.metadata


# # def run_migrations_offline() -> None:
# #     url = config.get_main_option("sqlalchemy.url")
# #     context.configure(
# #         url=url,
# #         target_metadata=target_metadata,
# #         literal_binds=True,
# #         dialect_opts={"paramstyle": "named"},
# #     )

# #     with context.begin_transaction():
# #         context.run_migrations()


# # def do_run_migrations(connection):
# #     context.configure(
# #         connection=connection,
# #         target_metadata=target_metadata,
# #     )

# #     with context.begin_transaction():
# #         context.run_migrations()


# # async def run_migrations_online() -> None:
# #     url = config.get_main_option("sqlalchemy.url") or settings.TEST_AUTH_DB_URL
# #     if url.startswith("postgresql+asyncpg"):
# #         sync_url = url.replace("postgresql+asyncpg", "postgresql+psycopg2")
# #     else:
# #         sync_url = url

# #     from sqlalchemy import create_engine

# #     connectable = create_engine(sync_url, poolclass=pool.NullPool)

# #     with connectable.connect() as connection:
# #         do_run_migrations(connection)


# # if context.is_offline_mode():
# #     run_migrations_offline()
# # else:
# #     asyncio.run(run_migrations_online())

# import asyncio
# import os
# import sys
# from logging.config import fileConfig

# from alembic import context
# from sqlalchemy import pool

# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# SRC_DIR = os.path.join(BASE_DIR, "src")
# if SRC_DIR not in sys.path:
#     sys.path.insert(0, SRC_DIR)

# from src.app.core.config import settings
# from src.app.db.base import Base
# from src.app.models.users import User  # noqa: F401
# from src.app.models.teams import Team  # noqa: F401
# from src.app.models.access_token import AccessToken  # noqa: F401

# config = context.config

# DB_URL = getattr(settings, "AUTH_DB_URL", None) or getattr(settings, "TEST_AUTH_DB_URL", None)
# if DB_URL:
#     config.set_main_option("sqlalchemy.url", DB_URL)

# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# # проверки целостности маппинга
# assert User.metadata is Base.metadata, "User.metadata != Base.metadata (разные Base)"
# assert Team.metadata is Base.metadata, "Team.metadata != Base.metadata (разные Base)"
# assert AccessToken.metadata is Base.metadata, "AccessToken.metadata != Base.metadata (разные Base)"

# target_metadata = Base.metadata
# if not target_metadata.tables:
#     raise RuntimeError("target_metadata.tables пуст — модели не загружены или Base не тот")

# def run_migrations_offline() -> None:
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#         compare_type=True,
#         compare_server_default=True,
#     )
#     with context.begin_transaction():
#         context.run_migrations()


# def do_run_migrations(connection):
#     context.configure(
#         connection=connection,
#         target_metadata=target_metadata,
#         compare_type=True,
#         compare_server_default=True,
#     )
#     with context.begin_transaction():
#         context.run_migrations()


# async def run_migrations_online() -> None:
#     url = config.get_main_option("sqlalchemy.url") or DB_URL
#     if url and url.startswith("postgresql+asyncpg"):
#         url = url.replace("postgresql+asyncpg", "postgresql+psycopg2")

#     from sqlalchemy import create_engine
#     connectable = create_engine(url, poolclass=pool.NullPool)

#     with connectable.connect() as connection:
#         do_run_migrations(connection)


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     asyncio.run(run_migrations_online())

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

from app.core.config import settings
from app.db.base import Base
from app.models.users import User  # noqa: F401
from app.models.teams import Team  # noqa: F401
from app.models.access_token import AccessToken  # noqa: F401

config = context.config
DB_URL = getattr(settings, "AUTH_DB_URL", None) or getattr(settings, "TEST_AUTH_DB_URL", None)
if DB_URL:
    config.set_main_option("sqlalchemy.url", DB_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

assert User.metadata is Base.metadata
assert Team.metadata is Base.metadata
assert AccessToken.metadata is Base.metadata

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
    connectable = create_engine(url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        do_run_migrations(connection)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
