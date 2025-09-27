from __future__ import annotations

from typing import Optional

from pydantic import Field, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # App settings
    APP_NAME: str = "matrix-guardian"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = Field(..., description="PostgreSQL URL for LangGraph checkpointer")

    # API endpoints
    MATRIXHUB_API_BASE: AnyHttpUrl = Field(..., description="Base URL for MatrixHub API")
    MATRIX_AI_BASE: AnyHttpUrl = Field(..., description="Base URL for the AI planning service")

    # HTTP client settings
    HTTP_TIMEOUT_SECONDS: float = 8.0
    HTTP_RETRIES: int = 2
    HTTP_BACKOFF: float = 0.5

    # Security
    API_TOKEN: Optional[str] = Field(None, description="Static bearer token for API auth")
    JWT_PUBLIC_KEY_PEM: Optional[str] = Field(None, description="PEM-encoded public key for JWT auth")

    # Sandbox execution environment
    SANDBOX_ALLOWED_HOSTS: str = "api.matrixhub.io"
    SANDBOX_CPU_LIMIT: int = 1
    SANDBOX_MEM_MB: int = 512
    SANDBOX_TIMEOUT_SEC: int = 30

    # AI model parameters
    AI_TEMPERATURE: float = 0.2
    AI_MAX_NEW_TOKENS: int = 256

# Instantiate settings once and export
settings = Settings()
