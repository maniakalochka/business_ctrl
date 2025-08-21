from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.base import engine

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=async_sessionmaker,
    expire_on_commit=True,
)
