import uvicorn
from fastapi import FastAPI

from app.auth.routers import (auth_router, register_router, reset_pwd_router,
                              users_router)

app = FastAPI(
    title="Auth Service",
    description="Service for user authentication",
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(register_router, prefix="/auth", tags=["auth"])
app.include_router(reset_pwd_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])



if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
