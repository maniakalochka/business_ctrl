from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import List, Optional


class TeamBase(BaseModel):
    name: str = Field(..., max_length=150, description="Название команды")
    slug: str = Field(..., max_length=150, description="Slug команды")


class TeamCreate(TeamBase):
    companies_id: UUID = Field(..., description="ID компании, к которой относится команда")


class TeamRead(TeamBase):
    id: UUID = Field(..., description="Уникальный идентификатор команды")
    companies_id: UUID = Field(..., description="ID компании, к которой относится команда")
    memberships: Optional[List] = Field(None, description="Список участников команды")

    model_config = ConfigDict(from_attributes=True)
