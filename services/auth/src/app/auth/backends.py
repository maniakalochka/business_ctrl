# backends.py
from fastapi_users.authentication import AuthenticationBackend
from .transports import bearer_transport
from app.auth.strategies import get_database_strategy

auth_backend_bearer = AuthenticationBackend(
    name="bearer-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
