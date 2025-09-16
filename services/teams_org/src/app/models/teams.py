import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.companies import Company
    from app.models.invites import Invite
    from app.models.memberships import Membership


class Team(Base):
    __tablename__ = "teams"

    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    owner_user_id: Mapped[uuid.UUID | None] = mapped_column(nullable=False)
    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )

    memberships: Mapped[list["Membership"]] = relationship(
        "Membership", back_populates="teams", cascade="all, delete-orphan"
    )

    companies: Mapped["Company"] = relationship(
        "Company",
        back_populates="teams",
        lazy="selectin",
    )

    invites: Mapped[list["Invite"]] = relationship(
        "Invite", back_populates="teams", cascade="all, delete-orphan"
    )
