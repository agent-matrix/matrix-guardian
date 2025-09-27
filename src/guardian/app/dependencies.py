import logging
import psycopg

from ..config import settings

logger = logging.getLogger(__name__)


def get_db_connection_status() -> bool:
    """Dependency to check the database connection status."""
    try:
        # The 'with' statement ensures the connection is closed.
        with psycopg.connect(settings.DATABASE_URL, connect_timeout=5) as conn:
            return not conn.closed
    except psycopg.OperationalError as e:
        logger.error(f"Database connection check failed: {e}")
        return False
