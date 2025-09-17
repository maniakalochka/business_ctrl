from typing import Sequence
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exceptions import AlreadyExists
from app.models.companies import Company
from app.repositories.base_sqlalchemy import SQLAlchemyRepository


class CompanyRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Company)

    async def get(self, company_id: UUID) -> Company | None:
        stmt = select(Company).where(Company.id == company_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

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
        exists = self.check_exists(name)
        if exists:
            raise AlreadyExists(f"Company with name '{name}' already exists.")
        async with self.session.begin():
            company = Company(name=name, owner_user_id=owner_id)
            self.session.add(company)
        return company

    async def set_active_atomic(self, company_name: str, is_active: bool) -> None:
        async with self.session.begin():
            stmt = (
                update(Company)
                .where(Company.name == company_name)
                .values(is_active=is_active)
            )
            await self.session.execute(stmt)
