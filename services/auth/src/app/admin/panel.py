from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.auth.manager import user_manager_context
from app.db.session import SessionLocal
from app.models.users import User


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")  # SQLAdmin по умолчанию передаёт username
        password = form.get("password")

        # o_O temporary credentials class, btw sqladmin should support this
        class Credentials:
            def __init__(self, username, password):
                self.username = username
                self.password = password

        credentials = Credentials(email, password)

        async with SessionLocal() as session:
            async with user_manager_context(session) as manager:
                user: User | None = await manager.authenticate(credentials)

                if user and user.is_active and user.role == "admin":
                    request.session["user_id"] = str(user.id)
                    return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("user_id"))


class UserAdminView(ModelView, model=User):
    class UserAdminView(ModelView, model=User):
        column_list = [User.id, User.email, User.role, User.is_active, User.created_at]
        column_searchable_list = [User.email, User.role]
        column_filters = [User.role, User.is_active]
        form_excluded_columns = [User.created_at, User.updated_at, User.hashed_password]
        can_create = True
        can_edit = True
        can_delete = True
        page_size = 20
        can_view_details = True
