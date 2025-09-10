import pytest
import datetime
from unittest.mock import AsyncMock
import uuid
import httpx
import pytest_asyncio
from asgi_lifespan import LifespanManager

from app.db import SessionLocal
from app.main import app


class FakePrincipal:
    def __init__(
        self,
        sub,
        role,
        scope,
    ):
        self.sub = sub
        self.role = role
        self.scope = scope


@pytest.fixture
def principal_admin() -> FakePrincipal:
    return FakePrincipal(
        sub="user1",
        role="admin",
        scope="companies.write",
    )


@pytest.fixture
def principal_manager() -> FakePrincipal:
    return FakePrincipal(
        sub="user1",
        role="manager",
        scope="teams.write",
    )


@pytest.fixture
def principal_employee() -> FakePrincipal:
    return FakePrincipal(sub="user2", role="employee", scope=[])


@pytest_asyncio.fixture
async def mock_team_service() -> AsyncMock:
    svc = AsyncMock()
    svc.create.return_value = {
        "id": str(uuid.uuid4()),
        "name": "Dev Team",
        "company_id": str(uuid.uuid4()),
        "is_active": True,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
    }
    return svc


@pytest_asyncio.fixture(scope="module")
async def test_app():
    async with LifespanManager(app):
        yield app


@pytest_asyncio.fixture
async def mock_company_service() -> AsyncMock:
    svc = AsyncMock()
    svc.create.return_value = {
        "id": str(uuid.uuid4()),
        "name": "TestCo",
        "owner_id": "user1",
        "is_active": True,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
    }
    return svc


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_client(test_app):
    transport = httpx.ASGITransport(app=test_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def session():
    async with SessionLocal() as s:
        yield s
