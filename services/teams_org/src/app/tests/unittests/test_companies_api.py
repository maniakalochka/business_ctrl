import pytest
from fastapi import status

from app.auth.deps import get_current_principal
from app.services.deps import company_service_dep


def override_principal(principal):
    async def _override():
        return principal

    return _override


def override_company_service(svc):
    return lambda: svc


@pytest.mark.asyncio
async def test_create_company_success(
    async_client, mock_company_service, principal_admin, test_app
) -> None:
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


@pytest.mark.asyncio
async def test_create_company_forbidden(
    async_client, mock_company_service, principal_employee, test_app
) -> None:
    test_app.dependency_overrides[get_current_principal] = override_principal(
        principal_employee
    )
    test_app.dependency_overrides[company_service_dep] = override_company_service(
        mock_company_service
    )
    response = await async_client.post("/companies/", params={"name": "TestCo"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Insufficient scope"
