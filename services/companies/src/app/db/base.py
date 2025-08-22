from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.db.session import SessionLocal

if settings.MODE == "TEST":
    DATABASE_URL = settings.COMPANY_DB_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.TEST_COMPANY_DB_URL
    DATABASE_PARAMS = {"poolclass": NullPool}


engine: AsyncEngine = create_async_engine(url=DATABASE_URL, echo=True, **DATABASE_PARAMS)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
