from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TeamBase(BaseModel):
    name: str = Field(..., max_length=150, description="Название команды")


class TeamCreate(TeamBase):
    owner_user_id: Optional[UUID] = Field(
        None, description="ID пользователя-владельца команды"
    )


class TeamRead(TeamBase):
    id: UUID = Field(..., description="Уникальный идентификатор команды")
    companies_id: UUID = Field(
        ..., description="ID компании, к которой относится команда"
    )
    memberships: Optional[List] = Field(None, description="Список участников команды")

    model_config = ConfigDict(from_attributes=True)


class TeamUpdate(BaseModel):
    name: str = Field(..., max_length=150, description="Новое название команды")
