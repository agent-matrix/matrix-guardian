"""Health probe monitoring API endpoints.

This module provides endpoints for monitoring health probes that check
the status of MCP servers and other infrastructure components.

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


@router.get("/probes", summary="List all health probes")
def list_probes() -> dict[str, Any]:
    """List all configured health probes and their current status.

    This endpoint returns information about all active health monitoring
    probes, including HTTP and MCP protocol probes with their latency
    and status information.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - probes (List[Dict]): List of probe objects with status information

    Example:
        >>> # GET /probes
        >>> {
        ...     "probes": [
        ...         {
        ...             "id": "pb_1",
        ...             "name": "Matrix-AI /readyz",
        ...             "type": "HTTP",
        ...             "status": "OK",
        ...             "latency": 45,
        ...             "last_check": "5s ago"
        ...         }
        ...     ]
        ... }
    """
    logger.debug("Listing all health probes")

    # TODO: Replace with actual probe data from database
    # For now, return mock data structure
    mock_probes = [
        {
            "id": "pb_1",
            "name": "Matrix-AI /readyz",
            "type": "HTTP",
            "status": "OK",
            "latency": 45,
            "last_check": "5s ago",
        },
        {
            "id": "pb_2",
            "name": "Matrix-Hub /health",
            "type": "HTTP",
            "status": "OK",
            "latency": 12,
            "last_check": "5s ago",
        },
        {
            "id": "pb_3",
            "name": "MCP: Echo Server",
            "type": "MCP",
            "status": "OK",
            "latency": 120,
            "last_check": "30s ago",
        },
        {
            "id": "pb_4",
            "name": "MCP: Postgres Tool",
            "type": "MCP",
            "status": "DEGRADED",
            "latency": 850,
            "last_check": "10s ago",
        },
    ]

    return {"probes": mock_probes}


__all__ = ["router"]
