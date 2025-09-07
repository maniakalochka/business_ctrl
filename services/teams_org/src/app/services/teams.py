from typing import Sequence
from uuid import UUID

from app.exceptions.exceptions import NotFound
from app.repositories.companies import CompanyRepository
from app.repositories.memberships import MembershipRepository
from app.repositories.teams import TeamRepository
from services.teams_org.src.app.models.teams import Team


class TeamService:
    def __init__(
        self,
        companies: CompanyRepository,
        teams: TeamRepository,
        memberships: MembershipRepository,
    ):
        self._companies = companies
        self._teams = teams
        self._memberships = memberships

    async def get(self, id_: UUID):
        return await self._companies.get(id_)

    async def create(
        self, *, company_id: UUID, name: str, owner_user_id: UUID | None = None
    ):
        company = await self._companies.get(company_id)
        if not company:
            raise NotFound("Компания не найдена")
        return await self._teams.create_team_atomic(
            company_id=company_id, name=name, owner_user_id=owner_user_id
        )

    async def rename(self, *, team_id: UUID, new_name: str) -> None:
        team = await self._teams.get(team_id)
        if not team:
            raise NotFound("Команда не найдена")
        await self._teams.rename_atomic(team_id=team_id, new_name=new_name)

    async def archive(self, team_id: UUID) -> None:
        team = await self._teams.get(team_id)
        if not team:
            raise NotFound("Команда не найдена")
        await self._memberships.archive_team_if_empty_atomic(team_id)

    async def list_by_company(
        self,
        company_id: UUID,
        *,
        only_active: bool = True,
        limit: int = 100,
        offset: int = 0
    ) -> Sequence[Team]:
        company = await self._companies.get(company_id)
        if not company:
            raise NotFound("Компания не найдена")
        return await self._teams.list_by_company(
            company_id=company_id, only_active=only_active, limit=limit, offset=offset
        )
