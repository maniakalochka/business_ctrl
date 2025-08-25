from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy

from app.auth.dependencies import get_access_token_db  # твой файл dependencies.py
from app.models.access_token import AccessToken
from app.core.config import settings


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        database=access_token_db,
        lifetime_seconds=settings.ACCESS_TOKEN_LIFETIME_SECONDS,
    )
