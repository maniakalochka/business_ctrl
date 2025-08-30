from __future__ import annotations
from uuid import UUID

from app.exceptions.exceptions import NotFound
from app.repositories.teams import TeamRepository
from app.repositories.memberships import MembershipRepository


class MembershipService:
    def __init__(self, teams: TeamRepository, memberships: MembershipRepository):
        self._teams = teams
        self._memberships = memberships

    async def add(self, *, team_id: UUID, user_id: UUID, role: str | None = "member") -> bool:
        team = await self._teams.get(team_id)
        if not team:
            raise NotFound("Команда не найдена")
        return await self._memberships.add_if_absent_atomic(team_id=team_id, user_id=user_id, role=role)

    async def remove(self, *, team_id: UUID, user_id: UUID) -> bool:
        team = await self._teams.get(team_id)
        if not team:
            raise NotFound("Команда не найдена")
        return await self._memberships.remove_if_present_atomic(team_id=team_id, user_id=user_id)

    async def change_role(self, *, team_id: UUID, user_id: UUID, role: str | None) -> None:
        team = await self._teams.get(team_id)
        if not team:
            raise NotFound("Команда не найдена")
        await self._memberships.change_role_atomic(team_id=team_id, user_id=user_id, role=role)

    async def list_members(self, team_id: UUID):
        team = await self._teams.get(team_id)
        if not team:
            raise NotFound("Команда не найдена")
        return await self._memberships.list_members(team_id)

    async def list_user_teams(self, user_id: UUID):
        return await self._memberships.list_user_teams(user_id)
