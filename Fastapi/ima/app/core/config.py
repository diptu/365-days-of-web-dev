# app/core/config.py
from __future__ import annotations

import json
from functools import lru_cache
from typing import Any
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str = Field(
        ...,
        validation_alias=AliasChoices(
            "DATABASE_URL", "IMA_DATABASE_URL", "ima_database_url"
        ),
    )
    APP_NAME: str = Field(
        default="IMA",
        validation_alias=AliasChoices("APP_NAME", "IMA_APP_NAME", "ima_app_name"),
    )
    DEBUG: bool = Field(
        default=False,
        validation_alias=AliasChoices("DEBUG", "IMA_DEBUG", "ima_debug"),
    )
    CORS_ORIGINS: list[str] = Field(
        default_factory=list,
        validation_alias=AliasChoices(
            "CORS_ORIGINS", "IMA_CORS_ORIGINS", "ima_cors_origins"
        ),
    )
    # ✅ NEW: testing mode toggle to influence app wiring (e.g., disable CORS)
    TESTING: bool = Field(
        default=False,
        validation_alias=AliasChoices("TESTING", "IMA_TESTING", "ima_testing"),
    )

    # Derived at runtime per instance
    ASYNCPG_SSL: bool = True

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, v: Any) -> list[str]:
        if v is None or v == "":
            return []
        if isinstance(v, list):
            return [str(x).strip() for x in v]
        s = str(v).strip()
        try:
            parsed = json.loads(s)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed]
        except json.JSONDecodeError:
            pass
        return [x.strip() for x in s.split(",") if x.strip()]

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def normalize_db_url(cls, v: str) -> str:
        url = v.strip()
        if url.startswith("postgres://"):
            url = "postgresql+asyncpg://" + url[len("postgres://") :]
        elif url.startswith("postgresql://"):
            url = "postgresql+asyncpg://" + url[len("postgresql://") :]

        parsed = urlparse(url)
        q = dict(parse_qsl(parsed.query, keep_blank_values=True))

        for k in (
            "sslmode",
            "channel_binding",
            "gssencmode",
            "target_session_attrs",
            "ssl",
        ):
            q.pop(k, None)

        new_query = urlencode(q)
        normalized = urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment,
            )
        )

        host = (parsed.hostname or "").lower()
        # local -> no SSL; remote -> SSL
        cls_default_ssl = host not in {"localhost", "127.0.0.1"}
        # store per-instance in model_post_init
        return normalized

    def model_post_init(self, __context: Any) -> None:  # type: ignore[override]
        parsed = urlparse(self.DATABASE_URL)
        host = (parsed.hostname or "").lower()
        self.ASYNCPG_SSL = host not in {"localhost", "127.0.0.1"}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
