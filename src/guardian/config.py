"""Matrix Guardian application configuration module.

This module defines the application settings using Pydantic Settings for
type-safe configuration management. Settings are loaded from environment
variables and .env files, with validation and type coercion.

The Settings class includes configuration for:
- Application basics (name, logging)
- Database connections
- External API endpoints
- HTTP client behavior
- Security settings
- Sandbox execution limits
- AI model parameters

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support.

    This class uses Pydantic Settings to load configuration from environment
    variables and .env files. All settings are validated and type-checked.

    Attributes:
        APP_NAME: Name of the application
        LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        DATABASE_URL: PostgreSQL connection URL for LangGraph checkpointer
        MATRIXHUB_API_BASE: Base URL for MatrixHub API endpoints
        MATRIX_AI_BASE: Base URL for the AI planning service
        HTTP_TIMEOUT_SECONDS: Default timeout for HTTP requests in seconds
        HTTP_RETRIES: Number of retry attempts for failed HTTP requests
        HTTP_BACKOFF: Backoff multiplier for exponential retry delays
        API_TOKEN: Optional static bearer token for API authentication
        JWT_PUBLIC_KEY_PEM: Optional PEM-encoded public key for JWT verification
        SANDBOX_ALLOWED_HOSTS: Comma-separated list of allowed hosts for sandbox
        SANDBOX_CPU_LIMIT: CPU limit for sandbox execution (cores)
        SANDBOX_MEM_MB: Memory limit for sandbox execution in megabytes
        SANDBOX_TIMEOUT_SEC: Maximum execution time for sandbox operations
        AI_TEMPERATURE: Temperature parameter for AI model (0.0-1.0)
        AI_MAX_NEW_TOKENS: Maximum number of tokens to generate

    Example:
        >>> settings = Settings()
        >>> print(settings.APP_NAME)
        'matrix-guardian'
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore",
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
    API_TOKEN: str | None = Field(None, description="Static bearer token for API auth")
    JWT_PUBLIC_KEY_PEM: str | None = Field(
        None, description="PEM-encoded public key for JWT auth",
    )

    # Sandbox execution environment
    SANDBOX_ALLOWED_HOSTS: str = "api.matrixhub.io"
    SANDBOX_CPU_LIMIT: int = 1
    SANDBOX_MEM_MB: int = 512
    SANDBOX_TIMEOUT_SEC: int = 30

    # AI model parameters
    AI_TEMPERATURE: float = 0.2
    AI_MAX_NEW_TOKENS: int = 256


# Instantiate settings once and export as singleton
settings: Settings = Settings()

__all__ = ["Settings", "settings"]
