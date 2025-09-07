import asyncio
import contextlib

from app.auth.dependencies import get_user_db
from app.auth.manager import get_user_manager
from app.db import get_async_session
from app.schemas.users import UserUpdate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def set_scope(email: str, scope: str):
    async with get_async_session_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                user = await user_manager.get_by_email(email)
                if user is None:
                    print("User not found")
                    return
                user_update = UserUpdate(scope=scope)
                # fastapi-users в этой версии ожидает (user_update, user)
                updated = await user_manager.update(user_update, user)
                print("Updated user scope:", getattr(updated, "scope", None))


if __name__ == "__main__":
    asyncio.run(
        set_scope("admin3@example.com", "companies.read companies.write teams.read")
    )
