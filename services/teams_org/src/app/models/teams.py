
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

import uuid
from app.db.base import Base


class Team(Base):
    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("company_id", "name", name="uq_team_company_name"),)

    name: Mapped[str] = mapped_column(String(150))
    slug: Mapped[str] = mapped_column(String(150))
    company_id: Mapped[uuid.UUID] = mapped_column(default=None, nullable=True)
