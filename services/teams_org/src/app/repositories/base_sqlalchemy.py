import uuid
from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession, model: Any):
        super().__init__(session, model)

    async def get(
            self,
            id_: uuid.UUID,
    ) -> Any | None:
        stmt = select(self.model).where(self.model.id == id_)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

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

    async def check_exists(self, obj: Any) -> bool:
        stmt = select(self.model).where(self.model.id == obj.id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None
