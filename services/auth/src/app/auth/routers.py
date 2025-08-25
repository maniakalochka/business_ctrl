from app.auth.backends import auth_backend_bearer
from app.schemas.users import UserCreate, UserRead, UserUpdate

from app.auth.manager import fastapi_users

auth_router = fastapi_users.get_auth_router(auth_backend_bearer)
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
verify_router = fastapi_users.get_verify_router(UserRead)
reset_pwd_router = fastapi_users.get_reset_password_router()
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
