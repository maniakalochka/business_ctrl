from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.abc import AbstactRepository


class SQLAlchemyRepository(AbstactRepository):
    def __init__(self, session: AsyncSession, model: Any):
        self.session = session
        self.model = model

    async def get(self, id_: Any):
        return await self.session.get(self.model, id_)

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
