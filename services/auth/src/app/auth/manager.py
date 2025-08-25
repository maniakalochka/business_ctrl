import logging
import uuid
from typing import Optional

from fastapi import Request
from fastapi_users import BaseUserManager, FastAPIUsers

from app.core.config import settings
from app.models.users import User

from .backends import auth_backend_bearer
from .dependencies import get_user_manager

log = logging.getLogger(__name__)

class UserManager(BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        log.warning("User %r has registered.", user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        log.warning("User %r has forgot their password. Reset token: %r", user.id, token)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        log.warning("Verification requested for user %r. Verification token: %r", user.id, token)


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend_bearer],
)

current_active_user = fastapi_users.current_user(active=True)
