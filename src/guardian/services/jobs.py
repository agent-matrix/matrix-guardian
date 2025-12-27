"""Jobs repository for optional task queue visibility.

This module provides a repository for tracking jobs in the 'jobs' table
of the additive database. It's designed to gracefully degrade if the table
doesn't exist, making it optional for deployment.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

import json
import logging
from typing import Any

import psycopg
from psycopg.rows import dict_row

from ..config import settings


logger = logging.getLogger(__name__)


class JobsRepo:
    """Optional repository for job queue visibility and tracking.

    This class provides methods to enqueue and update jobs in a PostgreSQL
    jobs table. If the table doesn't exist or is unavailable, all operations
    become no-ops that log debug messages and return None.

    This design allows the jobs feature to be optional without breaking
    the application.

    Attributes:
        dsn: PostgreSQL connection string (DSN)

    Example:
        >>> repo = JobsRepo()
        >>> job_id = repo.enqueue(kind="autopilot_check", state="queued")
        >>> if job_id:
        ...     repo.update(job_id, state="completed", output={"result": "ok"})
    """

    def __init__(self, dsn: str | None = None) -> None:
        """Initialize the jobs repository.

        Args:
            dsn: Optional PostgreSQL connection string. If None, uses
                settings.DATABASE_URL
        """
        self.dsn = dsn or settings.DATABASE_URL

    def _conn(self) -> psycopg.Connection:
        """Create a new database connection.

        Returns:
            psycopg.Connection: Database connection with autocommit enabled
                and dict_row factory for results

        Raises:
            psycopg.Error: If connection fails
        """
        return psycopg.connect(self.dsn, connect_timeout=5, autocommit=True, row_factory=dict_row)

    def enqueue(
        self, kind: str, state: str = "queued", input_: dict[str, Any] | None = None,
    ) -> int | None:
        """Enqueue a new job to the jobs table.

        This method inserts a new job record into the database. If the jobs
        table doesn't exist or the operation fails, it logs a debug message
        and returns None.

        Args:
            kind: Job kind/type identifier (e.g., "autopilot_check")
            state: Initial job state. Defaults to "queued"
            input_: Optional input data dictionary for the job

        Returns:
            Optional[int]: Job ID if successful, None if table doesn't exist
                or operation fails

        Raises:
            None: All exceptions are caught and logged

        Example:
            >>> repo = JobsRepo()
            >>> job_id = repo.enqueue(
            ...     kind="autopilot_check",
            ...     state="queued",
            ...     input_={"app_id": "app-123"}
            ... )
            >>> print(job_id)
            42
        """
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

    def update(self, job_id: int, state: str, output: dict[str, Any] | None = None) -> None:
        """Update an existing job's state and output.

        This method updates a job record in the database. If the jobs table
        doesn't exist or the operation fails, it logs a debug message and
        returns silently.

        Args:
            job_id: ID of the job to update
            state: New job state (e.g., "running", "completed", "failed")
            output: Optional output data dictionary from the job execution

        Returns:
            None

        Raises:
            None: All exceptions are caught and logged

        Example:
            >>> repo = JobsRepo()
            >>> repo.update(
            ...     job_id=42,
            ...     state="completed",
            ...     output={"result": "success", "issues_found": 3}
            ... )
        """
        try:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "UPDATE jobs SET state=%s, output=%s WHERE id=%s",
                    (state, json.dumps(output or {}), job_id),
                )
        except Exception as e:
            logger.debug("jobs.update skipped or failed: %s", e)


__all__ = ["JobsRepo"]
