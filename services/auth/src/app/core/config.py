from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    AUTH_DB_URL: str = (
        "postgresql+asyncpg://"
        + "postgres:password@localhost/"
        + "fastapi_users_db_sqlalchemy"
    )
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    MODE: Literal["DEV", "TEST"] = "TEST"

    # Auth
    ACCESS_TOKEN_LIFETIME_S: int
    RESET_PASSWORD_TOKEN_SECRET: str
    VERIFICATION_TOKEN_SECRET: str
    JWT_SECRET: str
    ALGO: str

    JWT_AUDIENCE: str
    JWT_ISSUER: str

    JWT_ACTIVE_KID: str

    INCLUDE_TEAM_IDS_IN_JWT: bool
    MAX_TEAMS_IN_JWT: int

    TEAMS_BASE_URL: str
    TEAMS_AUDIENCE: str

    REDIS_URL: str
    ORG_CLAIMS_CACHE_TTL_S: int
    INTROSPECT_TIMEOUT_S: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()  # type: ignore
