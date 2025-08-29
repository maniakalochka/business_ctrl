from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    COMPANY_DB_URL: str
    TEST_COMPANY_DB_URL: str

    MODE: Literal["DEV", "TEST"] = "TEST"

    SECRET: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()  # type: ignore
