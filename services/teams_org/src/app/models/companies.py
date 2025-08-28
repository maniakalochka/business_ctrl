from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
import uuid


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (UniqueConstraint("slug", name="uq_companies_slug"),)

    name: Mapped[str] = mapped_column(String(150))
    slug: Mapped[str] = mapped_column(String(150), unique=True)
    owner_user_id: Mapped[uuid.UUID] = mapped_column(default=None, nullable=True)
