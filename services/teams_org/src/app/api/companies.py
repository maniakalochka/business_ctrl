from fastapi import APIRouter, Depends, HTTPException, status

from app.services.companies import CompanyService
from app.schemas.companies import CompanyRead
from app.schemas.principal import Principal
from app.auth.deps import get_current_principal
from app.services.deps import company_service_dep


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

    company = await svc.create(name=name, owner_id=principal.sub)
    return CompanyRead.model_validate(company)
