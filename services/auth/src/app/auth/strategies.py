import time
import uuid
from typing import Any, Dict, Optional

import jwt
from app.models.users import User
from app.services.claims_client import load_org_claims
from fastapi import Request
from fastapi_users import models
from fastapi_users.authentication import JWTStrategy

from app.core.config import settings


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
        if request is not None:
            org = await load_org_claims(user.id, request)  # type: ignore
            if org:
                payload["company_id"] = org.get("company_id")
                if settings.INCLUDE_TEAM_IDS_IN_JWT:
                    payload["team_ids"] = org.get("team_ids") or []
                    payload["teams_truncated"] = org.get("teams_truncated", False)

        return jwt.encode(payload, self.secret, algorithm="HS256")


def get_jwt_strategy() -> JWTStrategy[User, uuid.UUID]:
    return IssuerJWTStrategy()
