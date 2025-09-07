import pytest
from fastapi import status
from unittest.mock import AsyncMock, MagicMock
from app.auth.deps import get_current_principal
from app.services.deps import company_service_dep
from datetime import datetime
import uuid


@pytest.fixture
def mock_company_service():
    svc = MagicMock()
    svc.create = AsyncMock(
        return_value={
            "id": str(uuid.uuid4()),
            "name": "TestCo",
            "owner_id": "user1",
            "is_active": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
    )
    return svc


def override_principal(principal):
    async def _override():
        return principal

    return _override


def override_company_service(svc):
    return lambda: svc


class Principal:
    def __init__(self, sub, role, scope):
        self.sub = sub
        self.role = role
        self.scope = scope


@pytest.fixture
def principal_admin():
    return Principal(sub="user1", role="admin", scope=["companies.write"])


@pytest.fixture
def principal_user():
    return Principal(sub="user2", role="user", scope=[])


@pytest.mark.asyncio
async def test_create_company_success(
    async_client, principal_admin, mock_company_service, test_app
):
    test_app.dependency_overrides[get_current_principal] = override_principal(
        principal_admin
    )
    test_app.dependency_overrides[company_service_dep] = override_company_service(
        mock_company_service
    )

    response = await async_client.post("/companies/", params={"name": "TestCo"})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "TestCo"
    assert data["id"] == mock_company_service.create.return_value["id"]

    test_app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_create_company_forbidden(
    async_client, principal_user, mock_company_service, test_app
):
    test_app.dependency_overrides[get_current_principal] = override_principal(
        principal_user
    )
    test_app.dependency_overrides[company_service_dep] = override_company_service(
        mock_company_service
    )

    response = await async_client.post("/companies/", params={"name": "TestCo"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Insufficient scope"

    test_app.dependency_overrides = {}
