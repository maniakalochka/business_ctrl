import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from app.main import app
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.db import SessionLocal
from app.db.base import Base
from unittest.mock import AsyncMock
from app.services.teams import TeamService
from sqlalchemy import text


# @pytest_asyncio.fixture(scope="session", autouse=True)
# async def engine():
#     engine = create_async_engine(settings.TEST_COMPANY_DB_URL, echo=False, pool_pre_ping=True)
#     async with engine.begin() as conn:
#         await conn.execute(text("CREATE SCHEMA IF NOT EXISTS teams_org;"))
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     yield engine
#     await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def test_app():
    async with LifespanManager(app):
        yield app


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_client(test_app):
    transport = httpx.ASGITransport(app=test_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def session():
    async with SessionLocal() as s:
        yield s

@pytest.fixture(scope="function", autouse=True)
def service():
    companies_repo = AsyncMock()
    teams_repo = AsyncMock()
    memberships_repo = AsyncMock()
    return TeamService(companies=companies_repo, teams=teams_repo, memberships=memberships_repo)
