import uuid
from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.models.users import User
from .backends import auth_backend_bearer
from typing import AsyncIterator


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncIterator[SQLAlchemyUserDatabase[User, uuid.UUID]]:
    yield SQLAlchemyUserDatabase(session, User)

class UserManager(BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = "unused-here"  # TODO: change it
    verification_token_secret = "unused-here"  # TODO: change it

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend_bearer],
)

current_active_user = fastapi_users.current_user(active=True)
