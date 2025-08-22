from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.teams import Team
from app.repositories.sql_repo import SQLAlchemyRepository

class TeamRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Team)

    async def by_slug(self, slug: str) -> Team | None:
        stmt = select(Team).where(Team.slug == slug)
        return await self.session.scalar(stmt)
