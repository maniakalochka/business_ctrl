import time
import jwt
from typing import Any, Dict, Optional
from fastapi_users.authentication import JWTStrategy
from fastapi_users import models
from app.core.config import settings
from app.services.claims_client import load_org_claims

from fastapi import Request


class IssuerJWTStrategy(JWTStrategy[models.UP, models.ID]):
    def __init__(self):
        super().__init__(settings.JWT_SECRET, settings.ACCESS_TOKEN_LIFETIME_S, settings.JWT_AUDIENCE)  # type: ignore

    async def write_token(self, user: models.UP, request: Optional[Request] = None) -> str:  # type: ignore
        now = int(time.time())
        payload: Dict[str, Any] = {
            "sub": str(user.id),
            "iat": now,
            "nbf": now - 5,
            "exp": now + self.lifetime_seconds,  # type: ignore
            "iss": settings.JWT_ISSUER,
            "aud": self.token_audience,
            "role": getattr(user, "role", None),
            "scope": getattr(user, "scope", None) or "companies.read teams.read",
        }

        org = None
        # fastapi-users login calls write_token(user) without request,
        # so load org claims only if request is provided
        if request is not None:
            org = await load_org_claims(user.id, request)  # type: ignore
            if org:
                payload["company_id"] = org.get("company_id")
                if settings.INCLUDE_TEAM_IDS_IN_JWT:
                    payload["team_ids"] = org.get("team_ids") or []
                    payload["teams_truncated"] = org.get("teams_truncated", False)

        return jwt.encode(payload, self.secret, algorithm="HS256")

    async def read_token(self, token: str, token_audience: Optional[str] = None) -> Dict[str, Any]:  # type: ignore
        return jwt.decode(
            token,
            self.secret,  # type: ignore
            algorithms=["HS256"],
            audience=self.token_audience,
            issuer=settings.JWT_ISSUER,
            options={"require": ["exp", "iat"]},
        )


def get_jwt_strategy():
    return IssuerJWTStrategy()
