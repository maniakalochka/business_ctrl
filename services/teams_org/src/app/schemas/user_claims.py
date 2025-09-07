from typing import Optional

from pydantic import BaseModel


class UserClaims(BaseModel):
    sub: str
    email: Optional[str] = None
    role: Optional[str] = None
    iss: Optional[str] = None
    aud: Optional[str] = None
    exp: int
