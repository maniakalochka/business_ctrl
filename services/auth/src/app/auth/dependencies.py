import uuid
from typing import AsyncIterator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import \
    SQLAlchemyAccessTokenDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.models.access_token import AccessToken
from app.models.users import User


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncIterator[SQLAlchemyUserDatabase[User, uuid.UUID]]:
    yield SQLAlchemyUserDatabase(session, User)

async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncIterator[SQLAlchemyAccessTokenDatabase[AccessToken]]:
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
