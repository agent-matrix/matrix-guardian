"""Health check and readiness probe API endpoints.

This module provides Kubernetes-style liveness and readiness probe endpoints
for monitoring the health and readiness of the Matrix Guardian service.

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

from fastapi import APIRouter, Depends

from ..dependencies import get_db_connection_status


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/healthz", summary="Liveness Probe")
def healthz() -> dict[str, bool]:
    """Liveness probe endpoint.

    This endpoint confirms that the service is running and able to respond
    to requests. It does not check downstream dependencies.

    Returns:
        Dict[str, bool]: A dictionary with an "ok" key set to True

    Example:
        >>> # GET /healthz
        >>> {"ok": true}
    """
    logger.debug("Healthz endpoint was called")
    return {"ok": True}


@router.get("/readyz", summary="Readiness Probe")
def readyz(db_ok: bool = Depends(get_db_connection_status)) -> dict[str, Any]:
    """Readiness probe endpoint.

    This endpoint checks if the service is ready to accept traffic by
    verifying that all downstream dependencies (like the database) are
    accessible and healthy.

    Args:
        db_ok: Database connection status injected via dependency

    Returns:
        Dict[str, Any]: A dictionary containing:
            - ok (bool): Overall readiness status
            - database_connected (bool): Database connection status

    Example:
        >>> # GET /readyz (when database is healthy)
        >>> {"ok": true, "database_connected": true}
        >>> # GET /readyz (when database is down)
        >>> {"ok": false, "database_connected": false}
    """
    if not db_ok:
        logger.warning("Readiness check failed: Database connection is down")
        return {"ok": False, "database_connected": False}

    logger.debug("Readiness check passed")
    return {"ok": True, "database_connected": True}


__all__ = ["router"]
