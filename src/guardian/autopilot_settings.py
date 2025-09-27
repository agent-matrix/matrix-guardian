from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class AutopilotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    enabled: bool = Field(default=False, alias="AUTOPILOT_ENABLED")
    api_enabled: bool = Field(default=False, alias="AUTOPILOT_API_ENABLED")
    interval_sec: int = Field(default=60, alias="AUTOPILOT_INTERVAL_SEC")
    policy_path: str = Field(default="src/guardian/agents/policies/default_policy.yaml", alias="AUTOPILOT_POLICY")
    safe_mode: bool = Field(default=True, alias="AUTOPILOT_SAFE_MODE")
