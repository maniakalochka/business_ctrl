"""
Create a superuser (or a common user)
"""

import asyncio
import contextlib

from fastapi_users.exceptions import UserAlreadyExists

from app.auth.dependencies import get_user_db
from app.auth.manager import get_user_manager
from app.db import get_async_session
from app.schemas.users import UserCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: str, password: str, is_superuser: bool = False, role: str = "admin"
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                            role=role,
                        )
                    )
                    print(f"User created {user}")
                    return user
    except UserAlreadyExists:
        print(f"User {email} already exists")
        raise


if __name__ == "__main__":
    asyncio.run(
        create_user(
            email="admin3@example.com", password="root", is_superuser=True, role="admin"
        )
    )
