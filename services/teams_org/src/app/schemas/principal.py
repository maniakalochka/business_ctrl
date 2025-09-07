from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Set, Literal


class Principal(BaseModel):
    sub: UUID
    email: Optional[str] = None
    role: Optional[Literal["admin", "manager", "employee"]] = None
    scope: Set[str] = set()
    company_id: Optional[UUID] = None
