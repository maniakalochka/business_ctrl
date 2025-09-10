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
