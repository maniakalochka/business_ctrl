import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.companies import Company
    from app.models.teams import Team


class MembershipStatus(str, enum.Enum):
    ACTIVE = "active"
    INVITED = "invited"
    PENDING = "pending"
    REMOVED = "removed"


class TeamRole(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class Membership(Base):
    __tablename__ = "memberships"

    team_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE")
    )
    user_id: Mapped[uuid.UUID] = mapped_column()
    companies_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id", name="fk_memberships_companies", ondelete="CASCADE"),
        index=True,
    )
    role: Mapped[TeamRole] = mapped_column(SQLEnum(TeamRole), default=TeamRole.MEMBER)
    status: Mapped[MembershipStatus] = mapped_column(
        SQLEnum(MembershipStatus), default=MembershipStatus.ACTIVE
    )
    inviter_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    joined_at: Mapped[datetime] = mapped_column(default=datetime.now)
    left_at: Mapped[datetime | None] = mapped_column(nullable=True)

    teams: Mapped["Team"] = relationship("Team", back_populates="memberships")
    companies: Mapped["Company"] = relationship("Company", back_populates="memberships")
