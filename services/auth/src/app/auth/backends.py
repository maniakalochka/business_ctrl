from fastapi_users.authentication import AuthenticationBackend
from .transports import cookie_transport, bearer_transport
from app.auth.strategies import get_jwt_strategy

auth_backend_cookie = AuthenticationBackend(
    name="cookie-jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

auth_backend_bearer = AuthenticationBackend(
    name="bearer-jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
