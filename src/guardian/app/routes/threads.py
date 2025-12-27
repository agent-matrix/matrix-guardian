"""Thread management API endpoints.

This module provides endpoints for listing and managing LangGraph workflow threads,
including paused threads awaiting human-in-the-loop (HITL) approval.

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

from fastapi import APIRouter


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/threads", summary="List all workflow threads")
def list_threads() -> dict[str, Any]:
    """List all workflow threads with their current status.

    This endpoint returns all active and paused LangGraph workflow threads,
    including their execution state, agent information, and pending approvals.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - threads (List[Dict]): List of thread objects with status information

    Example:
        >>> # GET /threads
        >>> {
        ...     "threads": [
        ...         {
        ...             "id": "th_8x992a",
        ...             "status": "PAUSED",
        ...             "agent": "RemediationAgent",
        ...             "node": "human_approval",
        ...             "created_at": "2m ago",
        ...             "risk_score": 85,
        ...             "summary": "High risk remediation plan proposed",
        ...             "plan": {...}
        ...         }
        ...     ]
        ... }
    """
    logger.debug("Listing all workflow threads")

    # TODO: Replace with actual database/checkpointer query
    # For now, return mock data structure
    mock_threads = [
        {
            "id": "th_8x992a",
            "status": "PAUSED",
            "agent": "RemediationAgent",
            "node": "human_approval",
            "created_at": "2m ago",
            "risk_score": 85,
            "summary": "High risk remediation plan proposed for Service: checkout-api",
            "plan": {
                "action": "scale_down",
                "target": "checkout-api",
                "reason": "Cost optimization anomaly detected",
                "impact": "Potential availability reduction during peak",
            },
        },
        {
            "id": "th_7b221c",
            "status": "RUNNING",
            "agent": "ObserverAgent",
            "node": "analyze_metrics",
            "created_at": "10s ago",
            "risk_score": 10,
            "summary": "Routine health probe analysis",
            "plan": None,
        },
        {
            "id": "th_3c445d",
            "status": "PAUSED",
            "agent": "PolicyAgent",
            "node": "policy_gate",
            "created_at": "15m ago",
            "risk_score": 60,
            "summary": "Configuration change request: ALLOWLIST_UPDATE",
            "plan": {
                "action": "update_config",
                "target": "firewall-rules",
                "reason": "New MCP server registration",
                "impact": "Security boundary modification",
            },
        },
    ]

    return {"threads": mock_threads}


__all__ = ["router"]
