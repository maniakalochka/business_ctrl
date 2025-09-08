import enum
import uuid
from datetime import datetime
from typing import Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="userrole", create_type=False), default=UserRole.EMPLOYEE
    )

    supervisor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    supervisor = relationship("User", remote_side="User.id", backref="subordinates")
