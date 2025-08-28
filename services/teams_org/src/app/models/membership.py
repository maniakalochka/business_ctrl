import enum
import uuid
from datetime import datetime
from sqlalchemy import UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Role(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"

class TeamMembership(Base):
    __tablename__ = "team_memberships"
    __table_args__ = (UniqueConstraint("user_id", "team_id", name="uq_membership"),)

    user_id: Mapped[uuid.UUID] = mapped_column(index=True)
    team_id: Mapped[uuid.UUID] = mapped_column(index=True)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.MEMBER)
    joined_at: Mapped[datetime] = mapped_column(default=datetime.now)
