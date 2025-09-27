from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

import psycopg
from psycopg.rows import dict_row

from ..config import settings

logger = logging.getLogger(__name__)


class JobsRepo:
    """
    OPTIONAL visibility/queue helper for the 'jobs' table (additive DB).
    If the table is absent, calls become no-ops.
    """

    def __init__(self, dsn: Optional[str] = None):
        self.dsn = dsn or settings.DATABASE_URL

    def _conn(self):
        return psycopg.connect(self.dsn, connect_timeout=5, autocommit=True, row_factory=dict_row)

    def enqueue(self, kind: str, state: str = "queued", input_: Optional[Dict[str, Any]] = None) -> Optional[int]:
        try:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO jobs(kind, state, input)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (kind, state, json.dumps(input_ or {})),
                )
                row = cur.fetchone()
                return int(row["id"]) if row else None
        except Exception as e:
            logger.debug("jobs.enqueue skipped or failed: %s", e)
            return None

    def update(self, job_id: int, state: str, output: Optional[Dict[str, Any]] = None) -> None:
        try:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "UPDATE jobs SET state=%s, output=%s WHERE id=%s",
                    (state, json.dumps(output or {}), job_id),
                )
        except Exception as e:
            logger.debug("jobs.update skipped or failed: %s", e)
