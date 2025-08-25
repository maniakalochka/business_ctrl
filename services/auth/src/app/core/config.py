from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)


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

    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8"
    )


settings = Settings()
