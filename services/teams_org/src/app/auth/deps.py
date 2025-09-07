import time
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import settings
from app.schemas.principal import Principal

bearer = HTTPBearer(auto_error=True)


def _decode(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGO],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
            options={"require": ["sub", "iss", "aud", "exp"]},
        )
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}"
        )


def get_current_principal(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
) -> Principal:
    payload = _decode(creds.credentials)
    now = int(time.time())
    if "nbf" in payload and payload["nbf"] - 10 > now:
        raise HTTPException(status_code=401, detail="Token not yet valid")

    scope_val = payload.get("scope", "")
    scopes = (
        set(scope_val.split()) if isinstance(scope_val, str) else set(scope_val or [])
    )
    return Principal(
        sub=payload["sub"],
        email=payload.get("email"),
        role=payload.get("role"),
        scope=scopes,
        company_id=payload.get("company_id"),
    )
