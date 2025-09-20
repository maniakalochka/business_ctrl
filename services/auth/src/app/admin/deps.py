from app.auth.manager import current_active_user
from app.models.users import User
from fastapi import Depends, HTTPException, status


async def current_admin_user(
    user: User = Depends(current_active_user),
) -> User:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return user
