import uuid
from datetime import datetime

from pydantic import BaseModel


class InviteCreateRequest(BaseModel):
    team_id: uuid.UUID
    email: str
    inviter_id: uuid.UUID


class InviteRead(BaseModel):
    id: uuid.UUID
    email: str
    team_id: uuid.UUID
    inviter_id: uuid.UUID
    token: str
    accepted: bool
    accepted_at: datetime | None

    class Config:
        from_attributes = True


class InviteAcceptRequest(BaseModel):
    token: str
