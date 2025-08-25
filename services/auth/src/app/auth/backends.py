# backends.py
from fastapi_users.authentication import AuthenticationBackend

from app.auth.strategies import get_database_strategy

from .transports import bearer_transport

auth_backend_bearer = AuthenticationBackend(
    name="bearer-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
