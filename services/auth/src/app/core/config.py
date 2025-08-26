from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    AUTH_DB_URL: str = (
        "postgresql+asyncpg://"
       +  "postgres:password@localhost/"
       +  "fastapi_users_db_sqlalchemy"
    )
    TEST_AUTH_DB_URL: str = (
        "postgresql+asyncpg://"
        + "postgres:password@localhost/"
        + "test_fastapi_users_db_sqlalchemy"
    )

    MODE: Literal["DEV", "TEST"] = "TEST"

    # Auth
    ACCESS_TOKEN_LIFETIME_SECONDS: int
    RESET_PASSWORD_TOKEN_SECRET: str
    VERIFICATION_TOKEN_SECRET: str
    SECRET: str
    ALGO: str = 'HS256'

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()  # type: ignore
