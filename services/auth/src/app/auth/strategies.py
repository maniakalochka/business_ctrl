from fastapi_users.authentication import JWTStrategy
from app.core.config import settings

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.AccessTtlSeconds,
    )
