from abc import ABC, abstractmethod
from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    def __init__(self, session: AsyncSession, model: Any):
        self.session = session
        self.model = model

    @abstractmethod
    async def get(self, id_: Any):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def list(self, *, limit: int, offset: int) -> Sequence[Any]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def add(self, obj: Any) -> Any:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def delete(self, obj: Any) -> None:
        raise NotImplementedError("Subclasses must implement this method")
