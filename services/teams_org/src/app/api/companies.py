from fastapi import APIRouter, Depends, HTTPException, status

from app.services.companies import CompanyService
from app.schemas.companies import CompanyRead, CompanyUpdate
from app.schemas.principal import Principal
from app.auth.deps import get_current_principal
from app.services.deps import company_service_dep
from app.exceptions.exceptions import AlreadyExists


cmp_router = APIRouter(tags=["companies"])


@cmp_router.post("/", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(
    name: str,
    principal: Principal = Depends(get_current_principal),
    svc: CompanyService = Depends(company_service_dep),
) -> CompanyRead:
    if "companies.write" not in principal.scope and (
        principal.role not in {"admin", "manager"}
    ):
        raise HTTPException(status_code=403, detail="Insufficient scope")
    try:
        company = await svc.create(name=name, owner_id=principal.sub)
    except AlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    return CompanyRead.model_validate(company)


@cmp_router.get("/{company_name}", response_model=CompanyRead)
async def read_company(
    company_name: str,
    principal: Principal = Depends(get_current_principal),
    svc: CompanyService = Depends(company_service_dep),
) -> CompanyRead:
    company = await svc.get(name=company_name)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    elif principal.role not in {"admin", "manager"}:
        raise HTTPException(status_code=403, detail="Access denied")
    return CompanyRead.model_validate(company)


@cmp_router.patch(
    "/{company_id}/deactivate",
    response_model=CompanyUpdate,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def deactivate_company(
    company_name: str,
    principal: Principal = Depends(get_current_principal),
    svc: CompanyService = Depends(company_service_dep),
) -> None:
    if "companies.write" not in principal.scope and (
        principal.role not in {"admin", "manager"}
    ):
        raise HTTPException(status_code=403, detail="Insufficient scope")
    await svc.deactivate(company_name=company_name)


async def activate_company(
    company_name: str,
    principal: Principal = Depends(get_current_principal),
    svc: CompanyService = Depends(company_service_dep),
) -> None:
    if "companies.write" not in principal.scope and (
        principal.role not in {"admin", "manager"}
    ):
        raise HTTPException(status_code=403, detail="Insufficient scope")
    await svc.activate(company_name=company_name)
