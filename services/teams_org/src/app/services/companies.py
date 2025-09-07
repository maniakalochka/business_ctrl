from typing import Sequence
from uuid import UUID

from app.exceptions.exceptions import NotFound
from app.repositories.companies import CompanyRepository
from app.repositories.teams import TeamRepository
from app.models.companies import Company
from app.models.teams import Team


class CompanyService:
    def __init__(self, companies: CompanyRepository, teams: TeamRepository):
        self._companies = companies
        self._teams = teams

    async def get(self, name: str) -> Company | None:
        return await self._companies.get_by_name(name=name)

    async def create(self, *, name: str, owner_id: UUID) -> Company:
        return await self._companies.create_atomic(name=name, owner_id=owner_id)

    async def activate(self, company_id: UUID) -> None:
        company = await self._companies.get(company_id)
        if not company:
            raise NotFound("Компания не найдена")
        await self._companies.set_active_atomic(company_id, True)

    async def deactivate(self, company_id: UUID) -> None:
        company = await self._companies.get(company_id)
        if not company:
            raise NotFound("Компания не найдена")
        await self._companies.set_active_atomic(company_id, False)

    async def list(
        self, *, limit: int = 100, offset: int = 0, is_active: bool | None = None
    ) -> Sequence:
        return await self._companies.list(is_active=is_active)

    async def list_teams(
        self,
        company_id: UUID,
        *,
        only_active: bool = True,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Team]:
        company = await self._companies.get(company_id)
        if not company:
            raise NotFound("Компания не найдена")
        return await self._teams.list_by_company(
            company_id, only_active=only_active, limit=limit, offset=offset
        )
