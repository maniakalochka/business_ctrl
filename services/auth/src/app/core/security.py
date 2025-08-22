from datetime import datetime, timedelta, timezone

from jose import jwt  # type: ignore
from passlib.context import CryptContext

from app.core.config import settings

pwd_ctx = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
ALGO = settings.ALGORITHM


def hash_password(p: str) -> str:
    return pwd_ctx.hash(p)


def verify_password(p: str, hashed: str) -> bool:
    return pwd_ctx.verify(p, hashed)


def create_token(sub: str, ttl_seconds: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=ttl_seconds)).timestamp()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGO)
