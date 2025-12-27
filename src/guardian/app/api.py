"""FastAPI application factory and configuration module.

This module creates and configures the FastAPI application instance for the
Matrix Guardian service. It sets up logging, includes routers for various
endpoints, and conditionally enables the autopilot router based on feature flags.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

import logging

from fastapi import FastAPI

from ..config import settings
from ..logging import setup_logging
from .routes import health as health_router
from .routes import resume as resume_router


# Initialize logging and settings
setup_logging(level=settings.LOG_LEVEL)

logger = logging.getLogger(__name__)

# Create FastAPI application instance
app: FastAPI = FastAPI(
    title=settings.APP_NAME, version="0.1.0", description="Matrix Guardian AI Control Plane",
)

# Include API routers
app.include_router(health_router.router, tags=["Health"])
app.include_router(resume_router.router, tags=["Workflows"])


@app.on_event("startup")
async def startup_event() -> None:
    """Execute startup tasks when the application starts.

    This function is called when the FastAPI application starts up.
    It can be extended to include initialization logic such as:
    - Connecting to message queues
    - Initializing database connections
    - Loading ML models
    - Starting background tasks

    Returns:
        None
    """
    logger.info("Matrix Guardian application starting up")
    # Placeholder for startup logic, e.g., connecting to a message queue


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Execute cleanup tasks when the application shuts down.

    This function is called when the FastAPI application is shutting down.
    It can be extended to include cleanup logic such as:
    - Closing database connections
    - Shutting down message queue connections
    - Saving state or metrics

    Returns:
        None
    """
    logger.info("Matrix Guardian application shutting down")


# Conditionally include autopilot router (feature-flagged)
try:
    from ..autopilot_settings import AutopilotSettings

    _ap_cfg = AutopilotSettings()
    if _ap_cfg.api_enabled:
        from .routes import autopilot as autopilot_router

        app.include_router(autopilot_router.router, tags=["Autopilot"])
        logger.info("Autopilot router enabled and loaded")
    else:
        logger.info("Autopilot router disabled via configuration")
except Exception as e:
    logger.warning(f"Autopilot router not loaded: {e}")


__all__ = ["app"]
