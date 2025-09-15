from typing import Sequence
from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exceptions import InvariantViolation
from app.models.teams import Team
from app.models.memberships import Membership
from app.repositories.base_sqlalchemy import SQLAlchemyRepository


class MembershipRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Membership)

    async def get(self, id_: UUID) -> Membership | None:
        stmt = select(Membership).where(Membership.id == id_)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID):
        stmt = select(Membership).where(Membership.user_id == user_id)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def list_members(self, team_id: UUID) -> Sequence[Membership]:
        stmt = select(Membership).where(Membership.team_id == team_id)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def list_user_teams(self, user_id: UUID) -> Sequence[Membership]:
        stmt = select(Membership).where(Membership.user_id == user_id)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def add_if_absent_atomic(
        self, *, team_id: UUID, user_id: UUID, role: str | None = "member"
    ) -> bool:
        async with self.session.begin():
            stmt = (
                pg_insert(Membership)
                .values(team_id=team_id, user_id=user_id, role=role)
                .on_conflict_do_nothing(
                    index_elements=[Membership.team_id, Membership.user_id]
                )
            )
            res = await self.session.execute(stmt)
            return res.rowcount == 1

    async def remove_if_present_atomic(self, *, team_id: UUID, user_id: UUID) -> bool:
        async with self.session.begin():
            stmt = delete(Membership).where(
                Membership.team_id == team_id, Membership.user_id == user_id
            )
            res = await self.session.execute(stmt)
            return res.rowcount > 0

    async def change_role_atomic(
        self, *, team_id: UUID, user_id: UUID, role: str | None
    ) -> None:
        async with self.session.begin():
            await self.session.execute(
                update(Membership)
                .where(Membership.team_id == team_id, Membership.user_id == user_id)
                .values(role=role)
            )

    async def archive_team_if_empty_atomic(self, team_id: UUID) -> None:
        async with self.session.begin():
            team = await self.session.get(Team, team_id, with_for_update=True)
            if team is None:
                return
            stmt_cnt = (
                select(func.count())
                .select_from(Membership)
                .where(Membership.team_id == team_id)
            )
            res_cnt = await self.session.execute(stmt_cnt)
            (count_members,) = res_cnt.one()
            if count_members and int(count_members) > 0:
                raise InvariantViolation
            await self.session.execute(
                update(Team).where(Team.id == team_id).values(is_active=False)
            )
