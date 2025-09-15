from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class InviteCreateRequest(BaseModel):
    email: EmailStr


class InviteRead(BaseModel):
    id: UUID
    email: EmailStr
    team_id: UUID
    inviter_id: UUID
    token: str
    accepted: bool
    accepted_at: datetime | None

    class Config:
        from_attributes = True


class InviteAcceptRequest(BaseModel):
    token: str
