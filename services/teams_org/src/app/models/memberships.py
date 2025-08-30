from typing import TYPE_CHECKING
import enum
from app.db.base import Base
from datetime import datetime
import uuid
from sqlalchemy import ForeignKey, UniqueConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
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
    __table_args__ = (
        UniqueConstraint("team_id", "user_id", name="uq_membership_team_user"),
        {"schema": "public"},
    )
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("public.teams.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column()
    role: Mapped[TeamRole] = mapped_column(SQLEnum(TeamRole), default=TeamRole.MEMBER)
    status: Mapped[MembershipStatus] = mapped_column(SQLEnum(MembershipStatus), default=MembershipStatus.ACTIVE)
    inviter_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    joined_at: Mapped[datetime] = mapped_column(default=datetime.now)
    left_at: Mapped[datetime | None] = mapped_column(nullable=True)

    team: Mapped["Team"] = relationship(back_populates="memberships")
