"""Configuration management API endpoints.

This module provides endpoints for viewing and managing system configuration,
including autopilot policy and environment settings.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

from ...autopilot_settings import AutopilotSettings
from ...config import settings


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/config", summary="Get system configuration")
def get_config() -> dict[str, Any]:
    """Get current system configuration and policy.

    This endpoint returns the current configuration flags and the autopilot
    policy YAML content.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - config (List[Dict]): List of configuration key-value pairs
            - policy (str): The autopilot policy YAML content

    Example:
        >>> # GET /config
        >>> {
        ...     "config": [
        ...         {"key": "AUTOPILOT_ENABLED", "value": "true", "type": "bool"},
        ...         {"key": "LOG_LEVEL", "value": "INFO", "type": "string"}
        ...     ],
        ...     "policy": "# Autopilot Policy\\n..."
        ... }
    """
    logger.debug("Fetching system configuration")

    try:
        ap_settings = AutopilotSettings()
    except Exception:
        ap_settings = None

    config_flags = [
        {
            "key": "AUTOPILOT_ENABLED",
            "value": str(ap_settings.enabled if ap_settings else False),
            "type": "bool",
        },
        {
            "key": "AUTOPILOT_SAFE_MODE",
            "value": str(ap_settings.safe_mode if ap_settings else True),
            "type": "bool",
        },
        {
            "key": "AUTOPILOT_INTERVAL_SEC",
            "value": str(ap_settings.interval_sec if ap_settings else 60),
            "type": "int",
        },
        {"key": "LOG_LEVEL", "value": settings.LOG_LEVEL, "type": "string"},
        {"key": "APP_NAME", "value": settings.APP_NAME, "type": "string"},
        {
            "key": "HTTP_TIMEOUT_SECONDS",
            "value": str(settings.HTTP_TIMEOUT_SECONDS),
            "type": "float",
        },
    ]

    # Load policy file
    policy_content = "# Policy file not found"
    if ap_settings:
        policy_path = Path(ap_settings.policy_path)
        if policy_path.exists():
            policy_content = policy_path.read_text()

    return {"config": config_flags, "policy": policy_content}


@router.put("/config", summary="Update system configuration")
def update_config(config_update: dict[str, Any]) -> dict[str, str]:
    """Update system configuration (placeholder).

    This endpoint is a placeholder for updating system configuration.
    In production, this would update environment variables or configuration files.

    Args:
        config_update: Dictionary of configuration updates

    Returns:
        Dict[str, str]: Status message

    Raises:
        HTTPException: 501 Not Implemented (placeholder endpoint)

    Example:
        >>> # PUT /config
        >>> # Body: {"AUTOPILOT_ENABLED": "true"}
        >>> {"status": "Configuration update not yet implemented"}
    """
    logger.warning(f"Configuration update requested but not implemented: {config_update}")
    raise HTTPException(
        status_code=501,
        detail="Configuration updates via API are not yet implemented. Please use environment variables.",
    )


__all__ = ["router"]
