import time
import uuid

import jwt

from app.core.config import settings


def generate_invite_token(
        *, team_id: uuid.UUID, inviter_id: uuid.UUID, email: str
) -> str:
    now = int(time.time())
    payload = {
        "sub": str(uuid.uuid4()),
        "team_id": str(team_id),
        "inviter_id": str(inviter_id),
        "email": email,
        "iat": now,
        "exp": now + settings.INVITE_TTL_SECONDS,
    }
    return jwt.encode(payload, settings.INVITE_SECRET, algorithm="HS256")


def verify_invite_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.INVITE_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Токен истёк")
    except jwt.InvalidTokenError:
        raise ValueError("Неверный токен")
