from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.membership import MembershipStatus, TeamRole


class MembershipBase(BaseModel):
    team_id: UUID = Field(..., description="ID команды")
    user_id: UUID = Field(..., description="ID пользователя")
    role: TeamRole = Field(..., description="Роль пользователя в команде")
    status: MembershipStatus = Field(..., description="Статус участия пользователя в команде")


class MembershipCreate(MembershipBase):
    inviter_id: Optional[UUID] = Field(None, description="ID пользователя, пригласившего участника")


class MembershipRead(MembershipBase):
    id: UUID = Field(..., description="Уникальный идентификатор участия")
    inviter_id: Optional[UUID] = Field(None, description="ID пользователя, пригласившего участника")
    joined_at: datetime = Field(..., description="Дата и время присоединения")
    left_at: Optional[datetime] = Field(None, description="Дата и время выхода")

    model_config = ConfigDict(from_attributes=True)
