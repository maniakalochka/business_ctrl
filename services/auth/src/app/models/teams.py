import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Team(Base):
    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("slug", name="uq_teams_slug"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150))
    slug: Mapped[str] = mapped_column(
        String(150)
    )  # человекочитаемый идентификатор
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    users = relationship(
        "User",
        back_populates="team",
        passive_deletes=True,
    )
