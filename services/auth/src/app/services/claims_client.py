import time
import jwt
from app.core.config import settings
import json
import httpx
from app.utils.redis import get_redis
from fastapi import Request


def _issue_m2m_token(scope: str) -> str:
    now = int(time.time())
    kid = settings.JWT_ACTIVE_KID
    secret = settings.JWT_SECRET
    payload = {
        "sub": "auth-service",
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "scope": scope,
        "iat": now,
        "nbf": now - 5,
        "exp": now + 60,
    }
    return jwt.encode(payload, secret, algorithm="HS256", headers={"kid": kid})


async def load_org_claims(user_id: str, request: Request) -> dict | None:
    r = await get_redis(request)
    key = f"orgclaims:{user_id}"
    cached = await r.get(key)
    if cached:
        return json.loads(cached)
    token = _issue_m2m_token("org.claims.read")
    url = f"{settings.TEAMS_BASE_URL}/internal/org-claims/{user_id}"
    async with httpx.AsyncClient(timeout=settings.INTROSPECT_TIMEOUT_S) as client:
        resp = await client.get(url, headers={"Authorization": f"Bearer {token}"})
    if resp.status_code != 200:
        return None
    data = resp.json()
    ttl = settings.ORG_CLAIMS_CACHE_TTL_S
    await r.set(key, json.dumps(data), ex=ttl)
    return data
