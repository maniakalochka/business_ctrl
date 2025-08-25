from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.repositories.sql_repo import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email) # type: ignore[reportArgumentType]
        return await self.session.scalar(stmt)
