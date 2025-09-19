from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    COMPANY_DB_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # Security
    JWT_SECRET: str
    ALGO: str
    JWT_ISSUER: str
    JWT_AUDIENCE: str
    CLOCK_SKEW_S: int

    # Cache
    REDIS_URL: str

    # Other
    INVITE_TTL_SECONDS: int = 60 * 60 * 24 * 7
    INVITE_SECRET: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()  # type: ignore
