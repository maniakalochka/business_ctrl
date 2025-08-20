from fastapi_users.db import SQLAlchemyBaseUserTable

from app.models.base import Base


class User(SQLAlchemyBaseUserTable, Base):
    pass
