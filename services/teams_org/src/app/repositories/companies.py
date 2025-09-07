from typing import Sequence
from uuid import UUID

from app.exceptions.exceptions import AlreadyExists
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.companies import Company
from src.app.repositories.base_sqlalchemy import SQLAlchemyRepository


class CompanyRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def get(self, company_id: UUID) -> Company | None:
    #     return await self.session.get(Company, company_id)
    # async def get_by_user_id(self, user_id: UUID) -> Company | None:
    #     stmt = (
    #         select(Company)
    #         .join_from(Company, Company.memberships)
    #         .where(Company.memberships.any(Company.memberships.user_id == user_id))
    #     )
    #     res = await self.session.execute(stmt)
    #     return res.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Company | None:
        stmt = select(Company).where(Company.name == name)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list(
        self, *, limit: int = 100, offset: int = 0, is_active: bool | None = None
    ) -> Sequence[Company]:
        stmt = select(Company)
        if is_active is not None:
            stmt = stmt.where(Company.is_active == is_active)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def create_atomic(self, *, name: str, owner_id: UUID) -> Company:
        try:
            async with self.session.begin():
                company = Company(name=name, owner_user_id=owner_id)
                self.session.add(company)
            return company
        except IntegrityError as e:
            raise AlreadyExists from e

    async def set_active_atomic(self, company_id: UUID, is_active: bool) -> None:
        async with self.session.begin():
            stmt = (
                update(Company)
                .where(Company.id == company_id)
                .values(is_active=is_active)
            )
            await self.session.execute(stmt)
