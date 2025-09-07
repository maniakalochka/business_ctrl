from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    COMPANY_DB_URL: str
    TEST_COMPANY_DB_URL: str

    MODE: Literal["DEV", "TEST"]

    # Security
    JWT_SECRET: str
    ALGO: str
    JWT_ISSUER: str
    JWT_AUDIENCE: str
    CLOCK_SKEW_S: int

    # Cache
    REDIS_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()  # type: ignore
