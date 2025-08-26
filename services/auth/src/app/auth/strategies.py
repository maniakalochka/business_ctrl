from fastapi_users.authentication import JWTStrategy

from app.core.config import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET,
        lifetime_seconds=settings.ACCESS_TOKEN_LIFETIME_SECONDS,
        algorithm=settings.ALGO,
        token_audience=["teams_org"]
    )
