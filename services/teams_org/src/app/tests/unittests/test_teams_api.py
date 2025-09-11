import uuid
import pytest
from fastapi import status
from app.auth.deps import get_current_principal
from app.services.deps import team_service_dep


def override_principal(principal):
    async def _override():
        return principal

    return _override


def override_team_service(svc):
    return lambda: svc


@pytest.mark.asyncio
async def test_create_team_success(
    async_client,
    mock_team_service,
    test_app,
    principal_manager,
):
    test_app.dependency_overrides[get_current_principal] = override_principal(
        principal_manager
    )
    test_app.dependency_overrides[team_service_dep] = override_team_service(
        mock_team_service
    )
    company_id = uuid.uuid4()
    owner_user_id = uuid.uuid4()
    response = await async_client.post(
        f"/companies/{company_id}/teams/",
        json={
            "companies_id": str(company_id),
            "name": "Dev Team",
            "owner_user_id": str(owner_user_id),
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Dev Team"
    assert data["id"] == mock_team_service.create.return_value["id"]


@pytest.mark.asyncio
async def test_only_admin_and_manager_can_create_team(
    async_client,
    mock_team_service,
    test_app,
    principal_employee,
):
    test_app.dependency_overrides[get_current_principal] = override_principal(
        principal_employee
    )
    test_app.dependency_overrides[team_service_dep] = override_team_service(
        mock_team_service
    )
    company_id = uuid.uuid4()
    owner_user_id = uuid.uuid4()
    response = await async_client.post(
        f"/companies/{company_id}/teams/",
        json={
            "companies_id": str(company_id),
            "name": "Dev Team",
            "owner_user_id": str(owner_user_id),
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_create_team_invalid_payload(
    async_client,
    mock_team_service,
    test_app,
    principal_manager,
):
    test_app.dependency_overrides[get_current_principal] = override_principal(
        principal_manager
    )
    test_app.dependency_overrides[team_service_dep] = override_team_service(
        mock_team_service
    )
    company_id = uuid.uuid4()
    # Missing required fields
    response = await async_client.post(
        f"/companies/{company_id}/teams/",
        json={"name": "Dev Team"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_rename_team_missing_name(
    async_client,
    mock_team_service,
    test_app,
    principal_admin,
):
    test_app.dependency_overrides[get_current_principal] = override_principal(
        principal_admin
    )
    test_app.dependency_overrides[team_service_dep] = override_team_service(
        mock_team_service
    )
    team_id = uuid.uuid4()
    company_id = uuid.uuid4()
    # Исправление: возвращаемое значение мока соответствует схеме TeamRead
    mock_team_service.rename.return_value = {
        "id": str(team_id),
        "name": "Some Name",
        "company_id": str(company_id),
        "owner_user_id": str(uuid.uuid4()),
    }
    response = await async_client.patch(
        f"/companies/{company_id}/teams/{team_id}/rename",
        json={},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_rename_team_forbidden_for_non_admin(
    async_client,
    mock_team_service,
    test_app,
    principal_employee,
):
    test_app.dependency_overrides[get_current_principal] = override_principal(
        principal_employee
    )
    test_app.dependency_overrides[team_service_dep] = override_team_service(
        mock_team_service
    )
    team_id = uuid.uuid4()
    company_id = uuid.uuid4()
    new_name = "Unauthorized Rename"
    response = await async_client.patch(
        f"/companies/{company_id}/teams/{team_id}/rename",
        json={"name": new_name},
    )
    assert response.status_code in [
        status.HTTP_403_FORBIDDEN,
        status.HTTP_401_UNAUTHORIZED,
    ]


@pytest.mark.asyncio
async def test_create_team_method_not_allowed(
    async_client,
    mock_team_service,
    test_app,
    principal_manager,
):
    test_app.dependency_overrides[get_current_principal] = override_principal(
        principal_manager
    )
    test_app.dependency_overrides[team_service_dep] = override_team_service(
        mock_team_service
    )
    company_id = uuid.uuid4()
    owner_user_id = uuid.uuid4()
    # PATCH is not allowed for create endpoint
    response = await async_client.patch(
        f"/companies/{company_id}/teams/",
        json={
            "companies_id": str(company_id),
            "name": "Dev Team",
            "owner_user_id": str(owner_user_id),
        },
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
