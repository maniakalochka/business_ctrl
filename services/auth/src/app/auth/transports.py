from fastapi_users.authentication import CookieTransport, BearerTransport

cookie_transport = CookieTransport(
    cookie_name="bc_auth",
    cookie_max_age=60 * 60 * 8,
    cookie_secure=True,
    cookie_httponly=True,
    cookie_samesite="lax",
)

bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")
