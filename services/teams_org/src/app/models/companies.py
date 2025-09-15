import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.memberships import Membership
    from app.models.teams import Team


class Company(Base):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    owner_user_id: Mapped[uuid.UUID] = mapped_column(nullable=False)

    memberships: Mapped[list["Membership"]] = relationship(
        "Membership",
        back_populates="companies",
        cascade="all, delete-orphan",
    )

    teams: Mapped[list["Team"]] = relationship(
        "Team",
        back_populates="companies",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
