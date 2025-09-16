import uuid

from app.exceptions.exceptions import NotFound
from app.models.invites import Invite
from app.repositories.invites import InviteRepository
from app.repositories.teams import TeamRepository
from app.utils.invites import generate_invite_token, verify_invite_token


class InvitesService:
    def __init__(self, teams: TeamRepository, invites: InviteRepository):
        self._teams = teams
        self._invites = invites

    async def check_invite_accepted(self, token: str) -> bool:
        invite = await self._invites.get_by_token(token)
        if not invite:
            raise NotFound("Инвайт не найден")
        return invite.accepted

    async def create_invite(
            self, *, team_id: uuid.UUID, email: str, inviter_id: uuid.UUID
    ) -> Invite:
        team = await self._teams.get(team_id)
        if not team:
            raise NotFound("Команда не найдена")

        token = generate_invite_token(
            team_id=team_id, inviter_id=inviter_id, email=email
        )

        invite = Invite(
            email=email,
            team_id=team_id,
            inviter_id=inviter_id,
            token=token,
            accepted=False,
            accepted_at=None,
        )

        return await self._invites.add(invite)

    async def accept_invite(self, *, token: str, user_id: uuid.UUID) -> Invite:
        payload = verify_invite_token(token)
        if not payload:
            raise ValueError("Неверный токен инвайта")
        invite = await self._invites.get_by_token(token)
        if not invite:
            raise NotFound("Инвайт не найден")
        if invite.accepted:
            raise ValueError("Инвайт уже был принят")

        return await self._invites.mark_accepted(invite)
