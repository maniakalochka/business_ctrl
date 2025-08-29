from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

class CompanyBase(BaseModel):
    name: str = Field(..., max_length=150)
    slug: str = Field(..., max_length=150)

class CompanyCreate(CompanyBase):
    owner_user_id: Optional[UUID] = Field(None)

class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    slug: Optional[str] = Field(None, max_length=150)
    is_active: Optional[bool] = Field(None)

class CompanyRead(CompanyBase):
    id: UUID = Field(...)
    owner_user_id: Optional[UUID] = Field(None)
    is_active: bool = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
