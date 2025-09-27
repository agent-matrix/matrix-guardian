import logging

from fastapi import APIRouter, Depends

from ..dependencies import get_db_connection_status

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/healthz", summary="Liveness Probe")
def healthz():
    """A simple endpoint to confirm the service is running."""
    logger.debug("Healthz endpoint was called.")
    return {"ok": True}


@router.get("/readyz", summary="Readiness Probe")
def readyz(db_ok: bool = Depends(get_db_connection_status)):
    """
    Checks if the service is ready to accept traffic, including
    downstream dependencies like the database.
    """
    if not db_ok:
        logger.warning("Readiness check failed: Database connection is down.")
        return {"ok": False, "database_connected": False}

    return {"ok": True, "database_connected": True}
