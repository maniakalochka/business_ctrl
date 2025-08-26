from fastapi_users.authentication import AuthenticationBackend

from app.auth.strategies import get_jwt_strategy
from app.auth.transports import bearer_transport


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
