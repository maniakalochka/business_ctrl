import jwt
from fastapi import HTTPException, Request

from app.core.config import settings


def _bearer(req: Request) -> str:
    a = req.headers.get("authorization", "")
    if not a.lower().startswith("bearer "):
        raise HTTPException(401, "missing bearer")
    return a.split(" ", 1)[1]


async def verify_service_token(request: Request):
    token = _bearer(request)
    try:
        secret = settings.JWT_SECRET
        claims = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
            options={"require": ["exp", "iat"]},
            leeway=settings.CLOCK_SKEW_S,
        )
    except jwt.InvalidTokenError:
        raise HTTPException(401, "invalid token")
    scopes = set((claims.get("scope") or "").split())
    if "org.claims.read" not in scopes or claims.get("sub") != "auth-service":
        raise HTTPException(403, "forbidden")
    return claims
