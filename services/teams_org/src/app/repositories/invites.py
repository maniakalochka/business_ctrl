import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invites import Invite
from app.repositories.base_sqlalchemy import SQLAlchemyRepository


class InviteRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Invite)

    async def create_atomic(self, *, email: str, team_id: uuid.UUID) -> Invite:
        exists = await self.check_exists(Invite)
        async with self.session.begin():
            invite = Invite(email=email, team_id=team_id)
            self.session.add(invite)
        return invite

    async def get_by_token(self, token: str) -> Invite | None:
        stmt = select(Invite).where(Invite.token == token)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def mark_accepted(self, invite: Invite) -> Invite:
        invite.accepted = True
        invite.accepted_at = datetime.datetime.now()
        await self.session.commit()
        await self.session.refresh(invite)
        return invite
