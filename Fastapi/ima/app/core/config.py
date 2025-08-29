# app/core/config.py
from typing import List, Optional
from pydantic import Field, AliasChoices, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "IMA"
    debug: bool = True

    # Accept JSON for list envs: CORS_ORIGINS='["http://localhost:3000"]'
    cors_origins: List[str] = ["http://localhost:3000"]

    # Accepts IMA_DATABASE_URL or DATABASE_URL from env; falls back to default
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/ima",
        validation_alias=AliasChoices("IMA_DATABASE_URL", "DATABASE_URL"),
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="IMA_",  # prefer IMA_* but allow fallbacks via AliasChoices
        extra="ignore",
    )

    @field_validator("database_url")
    @classmethod
    def validate_db_url(cls, v: str) -> str:
        allowed = (
            "postgresql://",
            "postgresql+asyncpg://",
            "postgresql+psycopg://",
            "postgresql+psycopg2://",
        )
        if not v.startswith(allowed):
            raise ValueError(
                "database_url must start with one of: "
                "postgresql://, postgresql+asyncpg://, "
                "postgresql+psycopg://, postgresql+psycopg2://"
            )
        # Quick guard against accidental double '?'
        if v.count("?") > 1:
            raise ValueError("database_url has multiple '?' characters; fix query part")
        return v


settings = Settings()
