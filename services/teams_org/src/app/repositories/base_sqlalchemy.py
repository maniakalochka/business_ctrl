from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession, model: Any):
        super().__init__(session, model)

    async def list(self, *, limit: int = 100, offset: int = 0) -> Sequence[Any]:
        stmt = select(self.model).limit(limit).offset(offset)
        return (await self.session.execute(stmt)).scalars().all()

    async def add(self, obj: Any) -> Any:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: Any) -> None:
        await self.session.delete(obj)
        await self.session.commit()
