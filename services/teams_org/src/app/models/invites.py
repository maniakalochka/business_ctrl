import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.teams import Team


class Invite(Base):
    __tablename__ = "invites"

    email: Mapped[str] = mapped_column(nullable=False, index=True)  # target email
    team_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), index=True
    )
    inviter_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    accepted: Mapped[bool] = mapped_column(default=False)
    accepted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    teams: Mapped["Team"] = relationship("Team", back_populates="invites")
