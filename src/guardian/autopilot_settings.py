"""Autopilot configuration settings module.

This module defines the autopilot-specific configuration using Pydantic Settings.
The autopilot system enables automated monitoring and response capabilities
with configurable intervals, policies, and safety modes.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AutopilotSettings(BaseSettings):
    """Autopilot configuration with environment variable support.

    This class manages autopilot-specific settings including enable/disable flags,
    execution intervals, policy paths, and safety controls.

    Attributes:
        enabled: Whether autopilot is enabled for background execution
        api_enabled: Whether autopilot API endpoints are accessible
        interval_sec: Interval in seconds between autopilot checks
        policy_path: File path to the YAML policy configuration
        safe_mode: When True, restricts autopilot to read-only operations

    Example:
        >>> autopilot_settings = AutopilotSettings()
        >>> print(autopilot_settings.enabled)
        False
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    enabled: bool = Field(
        default=False, alias="AUTOPILOT_ENABLED", description="Enable autopilot background worker",
    )
    api_enabled: bool = Field(
        default=False, alias="AUTOPILOT_API_ENABLED", description="Enable autopilot API endpoints",
    )
    interval_sec: int = Field(
        default=60,
        alias="AUTOPILOT_INTERVAL_SEC",
        description="Autopilot check interval in seconds",
    )
    policy_path: str = Field(
        default="src/guardian/agents/policies/default_policy.yaml",
        alias="AUTOPILOT_POLICY",
        description="Path to autopilot policy YAML file",
    )
    safe_mode: bool = Field(
        default=True,
        alias="AUTOPILOT_SAFE_MODE",
        description="Enable safe mode (read-only operations)",
    )


__all__ = ["AutopilotSettings"]
