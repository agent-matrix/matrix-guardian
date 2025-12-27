"""FastAPI dependency injection functions module.

This module provides dependency injection functions for FastAPI endpoints,
including database connection health checks and other shared dependencies.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

import logging

import psycopg

from ..config import settings


logger = logging.getLogger(__name__)


def get_db_connection_status() -> bool:
    """Check the database connection status.

    This dependency function attempts to connect to the PostgreSQL database
    using the configured DATABASE_URL. It's primarily used for health check
    and readiness probe endpoints.

    Returns:
        bool: True if database connection is successful and open, False otherwise

    Raises:
        None: Exceptions are caught and logged, returning False instead

    Example:
        >>> from fastapi import Depends
        >>> @app.get("/readyz")
        >>> def readiness(db_ok: bool = Depends(get_db_connection_status)):
        ...     return {"database_connected": db_ok}
    """
    try:
        # The 'with' statement ensures the connection is properly closed
        with psycopg.connect(settings.DATABASE_URL, connect_timeout=5) as conn:
            is_open = not conn.closed
            if is_open:
                logger.debug("Database connection check successful")
            else:
                logger.warning("Database connection is closed")
            return is_open
    except psycopg.OperationalError as e:
        logger.error(f"Database connection check failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during database connection check: {e}")
        return False


__all__ = ["get_db_connection_status"]
