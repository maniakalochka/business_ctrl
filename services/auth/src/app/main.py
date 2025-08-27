import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer

from app.auth.routers import (auth_router, register_router, reset_pwd_router,
                              users_router, verify_router)
from app.db.session import SessionLocal, engine

http_bearer = HTTPBearer(auto_error=False)

log = logging.getLogger(__name__)

@asynccontextmanager  # type: ignore
async def lifespan(app: FastAPI):
    log.info("Starting up...")
    app.state.engine = engine
    app.state.session_factory = SessionLocal
    yield
    log.info("Shutting down...")
    await engine.dispose()


app = FastAPI(
    title="Auth Service",
    description="Service for user authentication",
    lifespan=lifespan,
)

app.include_router(auth_router, prefix="/auth/jwt", tags=["auth"], dependencies=[Depends(http_bearer)])
app.include_router(register_router, prefix="/auth", tags=["auth"])
app.include_router(reset_pwd_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(verify_router, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
