from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Load app config from .env (Pydantic v2 style).
    """

    # where & how to load env vars
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # env-driven fields
    APP_NAME: str = "Fast-multitenecy"
    DEBUG: bool = False
    DATABASE_URL: str  # keep as str to avoid strict DSN validation surprises
    MONGO_DB: str = "multitenecy"

    # app-specific defaults
    DEV_DEFAULT_TENANT_SCHEMA: str = "tenant_default"

    @field_validator("DATABASE_URL")
    @classmethod
    def _validate_db_url(cls, v: str) -> str:
        if not v.startswith(("postgresql://", "postgresql+psycopg2://")):
            raise ValueError(
                "DATABASE_URL must start with postgresql:// or postgresql+psycopg2://"
            )
        return v


settings = Settings()
