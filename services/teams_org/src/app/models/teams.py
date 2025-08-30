
from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

import uuid
from app.db.base import Base

from sqlalchemy.orm import relationship


if TYPE_CHECKING:
    from app.models.memberships import Membership
    from app.models.companies import Company

class Team(Base):
    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("companies_id", "name", name="uq_team_company_name"), {"schema": "teams_org"})

    name: Mapped[str] = mapped_column(String(150))
    slug: Mapped[str] = mapped_column(String(150))
    companies_id: Mapped[uuid.UUID] = mapped_column(
            ForeignKey("teams_org.companies.id", ondelete="CASCADE"), nullable=False
        )

    memberships: Mapped[list["Membership"]] = relationship(
            back_populates="team", cascade="all, delete-orphan"
        )

    companies: Mapped["Company"] = relationship(
            back_populates="teams",
            lazy="selectin",
        )
