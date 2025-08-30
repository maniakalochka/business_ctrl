import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


if TYPE_CHECKING:
    from app.models.teams import Team


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (UniqueConstraint(
        "slug",
        name="uq_companies_slug"), {"schema": "public"},)

    name: Mapped[str] = mapped_column(String(150))
    slug: Mapped[str] = mapped_column(String(150), unique=True)
    owner_user_id: Mapped[uuid.UUID] = mapped_column(default=None, nullable=True)

    teams: Mapped[list["Team"]] = relationship(
            back_populates="company",
            cascade="all, delete-orphan",
            lazy="selectin",
        )
