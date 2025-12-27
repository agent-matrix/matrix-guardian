"""Autopilot API endpoints.

This module provides REST API endpoints for the autopilot functionality,
allowing manual triggering of autopilot planning cycles and status checks.
The autopilot system automates infrastructure monitoring and response based
on configured policies.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from ...agents.autopilot import Autopilot
from ...agents.policy import Policy
from ...autopilot_settings import AutopilotSettings
from ...services.matrix_ai_client import MatrixAIClient
from ...services.matrix_hub_client import MatrixHubClient


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/autopilot/status")
async def autopilot_status() -> dict[str, Any]:
    """Get current autopilot configuration and status.

    This endpoint returns the current autopilot settings including whether
    it's enabled, the check interval, policy path, and safe mode status.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - enabled (bool): Whether autopilot is enabled
            - api_enabled (bool): Whether autopilot API is enabled
            - interval_sec (int): Check interval in seconds
            - policy_path (str): Path to the policy YAML file
            - safe_mode (bool): Whether safe mode is enabled

    Example:
        >>> # GET /autopilot/status
        >>> {
        ...     "enabled": false,
        ...     "api_enabled": true,
        ...     "interval_sec": 60,
        ...     "policy_path": "src/guardian/agents/policies/default_policy.yaml",
        ...     "safe_mode": true
        ... }
    """
    cfg = AutopilotSettings()
    logger.debug("Autopilot status requested")
    return {
        "enabled": cfg.enabled,
        "api_enabled": cfg.api_enabled,
        "interval_sec": cfg.interval_sec,
        "policy_path": cfg.policy_path,
        "safe_mode": cfg.safe_mode,
    }


@router.post("/autopilot/plan-once")
async def autopilot_plan_once(
    target_uid: str | None = Query(
        default=None, description="Optional target UID to focus planning on a specific resource",
    ),
) -> dict[str, Any]:
    """Execute a single autopilot planning cycle.

    This endpoint manually triggers one autopilot planning cycle, optionally
    focusing on a specific resource identified by target_uid. The autopilot
    will analyze the current infrastructure state, compare it against the
    policy, and generate recommended actions.

    Args:
        target_uid: Optional unique identifier of a specific resource to analyze.
            If not provided, autopilot will analyze all monitored resources.

    Returns:
        Dict[str, Any]: The result of the planning cycle, including identified
            issues and recommended actions

    Raises:
        HTTPException: 403 error if AUTOPILOT_API_ENABLED is set to false

    Example:
        >>> # POST /autopilot/plan-once
        >>> {
        ...     "status": "completed",
        ...     "issues_found": 2,
        ...     "actions_recommended": ["restart_service", "scale_up"]
        ... }
    """
    cfg = AutopilotSettings()

    if not cfg.api_enabled:
        logger.warning("Autopilot API endpoint accessed but API is disabled")
        raise HTTPException(
            status_code=403, detail="Autopilot API is disabled (AUTOPILOT_API_ENABLED=false)",
        )

    try:
        logger.info(
            "Manually triggered autopilot planning cycle"
            + (f" for target_uid={target_uid}" if target_uid else ""),
        )

        # Initialize clients and policy
        hub = MatrixHubClient()
        ai = MatrixAIClient()
        policy = Policy.from_yaml(cfg.policy_path)
        policy.safe_mode = cfg.safe_mode

        # Create and run autopilot instance
        ap = Autopilot(hub_client=hub, ai_client=ai, policy=policy, settings=cfg)

        result = await ap.run_once(target_uid=target_uid)
        logger.info(f"Autopilot planning cycle completed: {result}")
        return result

    except Exception as e:
        logger.error(f"Autopilot planning cycle failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Autopilot planning failed: {e!s}")


__all__ = ["router"]
