import uvicorn
from fastapi import FastAPI
from app.auth.routers import (
    auth_router,
    register_router,
    # reset_pwd_router,
    # users_router,
    # verify_router,
)

app = FastAPI(
    title="Auth Service",
    description="Service for user authentication and management",
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(register_router, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
