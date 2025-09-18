import uuid
from typing import Sequence

from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.exceptions.exceptions import AlreadyExists
from app.models.teams import Team
from app.repositories.base_sqlalchemy import SQLAlchemyRepository


class TeamRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Team)

    async def get(self, team_id: uuid.UUID) -> Team | None:
        stmt = (
            select(Team)
            .options(
                selectinload(Team.memberships),
                selectinload(Team.invites),
                selectinload(Team.companies),
            )
            .where(Team.id == team_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_name_in_company(
            self, *, name: str, company_id: uuid.UUID
    ) -> Team | None:
        stmt = (
            select(Team)
            .options(
                selectinload(Team.memberships),
                selectinload(Team.invites),
                selectinload(Team.companies),
            )
            .where(Team.company_id == company_id)
            .where(func.lower(Team.name) == func.lower(name))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_by_company(
            self,
            company_id: uuid.UUID,
            *,
            only_active: bool = True,
            limit: int = 100,
            offset: int = 0
    ) -> Sequence[Team]:
        stmt = (
            select(Team)
            .options(
                selectinload(Team.memberships),
                selectinload(Team.invites),
                selectinload(Team.companies),
            )
            .where(Team.company_id == company_id)
        )
        if only_active:
            stmt = stmt.where(Team.is_active.is_(True))
        stmt = stmt.limit(limit).offset(offset)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def create_team_atomic(
            self, *, company_id: uuid.UUID, name: str, owner_user_id: uuid.UUID | None
    ) -> Team:
        team = Team(company_id=company_id, name=name, owner_user_id=owner_user_id)
        try:
            self.session.add(team)
            await self.session.flush()
            await self.session.commit()
            return await self.get(team.id)
        except IntegrityError as e:
            raise AlreadyExists from e

    async def rename_atomic(self, *, team_id: uuid.UUID, new_name: str) -> None:
        try:
            async with self.session.begin():
                await self.session.execute(
                    update(Team).where(Team.id == team_id).values(name=new_name)
                )
        except IntegrityError as e:
            raise AlreadyExists from e

    async def set_active(self, team_id: uuid.UUID, is_active: bool) -> None:
        async with self.session.begin():
            await self.session.execute(
                update(Team).where(Team.id == team_id).values(is_active=is_active)
            )
