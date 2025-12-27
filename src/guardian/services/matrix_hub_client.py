"""MatrixHub API client for application discovery and event recording.

This module provides an async HTTP client for interacting with the Matrix-Hub
API. It supports application discovery, health status updates, and event
recording with automatic retries and error handling.

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

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import settings


logger = logging.getLogger(__name__)


def _auth_headers() -> dict[str, str]:
    """Generate authentication headers for API requests.

    Returns:
        Dict[str, str]: Headers dictionary with Authorization header if
            API_TOKEN is configured, otherwise empty dict

    Example:
        >>> headers = _auth_headers()
        >>> print(headers.get("Authorization"))
        'Bearer abc123...'
    """
    headers: dict[str, str] = {}
    if settings.API_TOKEN:
        headers["Authorization"] = f"Bearer {settings.API_TOKEN}"
    return headers


class MatrixHubClient:
    """Async HTTP client for Matrix-Hub API operations.

    This client provides methods for discovering applications, updating health
    status, and recording events in the Matrix-Hub system. All methods include
    automatic retry logic with exponential backoff.

    Attributes:
        base_url: Base URL for the Matrix-Hub API
        timeout: HTTP request timeout in seconds

    Example:
        >>> client = MatrixHubClient()
        >>> apps = await client.list_apps(limit=50)
        >>> print(len(apps))
        50
    """

    def __init__(self, base_url: str | None = None, timeout: float | None = None) -> None:
        """Initialize the MatrixHub client.

        Args:
            base_url: Optional base URL override. If None, uses
                settings.MATRIXHUB_API_BASE
            timeout: Optional timeout override in seconds. If None, uses
                settings.HTTP_TIMEOUT_SECONDS
        """
        self.base_url = (base_url or str(settings.MATRIXHUB_API_BASE)).rstrip("/")
        self.timeout = timeout or float(settings.HTTP_TIMEOUT_SECONDS)

    # ---------- Read Operations ----------

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    async def list_apps(self, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        """List applications from Matrix-Hub with pagination.

        Args:
            limit: Maximum number of applications to return. Defaults to 100.
            offset: Pagination offset. Defaults to 0.

        Returns:
            List[Dict[str, Any]]: List of application dictionaries

        Raises:
            httpx.HTTPError: If the request fails after all retries

        Example:
            >>> apps = await client.list_apps(limit=50, offset=0)
            >>> for app in apps:
            ...     print(app["uid"])
        """
        url = f"{self.base_url}/apps"
        async with httpx.AsyncClient(timeout=self.timeout, headers=_auth_headers()) as client:
            resp = await client.get(url, params={"limit": limit, "offset": offset})
            resp.raise_for_status()
            data = resp.json() or {}
            return data.get("items", [])

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    async def get_app_or_none(self, uid: str) -> dict[str, Any] | None:
        """Retrieve a specific application by UID.

        Args:
            uid: Unique identifier of the application

        Returns:
            Optional[Dict[str, Any]]: Application dictionary if found,
                None if not found (404)

        Raises:
            httpx.HTTPError: If the request fails with non-404 error
                after all retries

        Example:
            >>> app = await client.get_app_or_none("app-123")
            >>> if app:
            ...     print(app["name"])
        """
        url = f"{self.base_url}/apps/{uid}"
        async with httpx.AsyncClient(timeout=self.timeout, headers=_auth_headers()) as client:
            resp = await client.get(url)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()

    # ---------- Write Operations ----------

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    async def upsert_status(
        self,
        entity_uid: str,
        score: float | None,
        status: str | None,
        last_checked_iso: str | None,
        check: str | None,
        result: str | None,
        latency_ms: float | None,
        reasons: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Upsert health status for an entity in Matrix-Hub.

        Args:
            entity_uid: Unique identifier of the entity
            score: Health score (0.0-1.0)
            status: Status string (e.g., "healthy", "unhealthy")
            last_checked_iso: ISO timestamp of the last check
            check: Check type identifier
            result: Check result details
            latency_ms: Check latency in milliseconds
            reasons: Optional dictionary of reasons/details
            idempotency_key: Optional idempotency key for safe retries

        Returns:
            Dict[str, Any]: Response from the API

        Raises:
            httpx.HTTPError: If the request fails after all retries

        Example:
            >>> result = await client.upsert_status(
            ...     entity_uid="app-123",
            ...     score=0.95,
            ...     status="healthy",
            ...     last_checked_iso="2025-01-15T10:30:00Z",
            ...     check="http_probe",
            ...     result="200 OK",
            ...     latency_ms=45.2
            ... )
        """
        url = f"{self.base_url}/status"
        headers = _auth_headers()
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        payload = {
            "entity_uid": entity_uid,
            "score": score,
            "status": status,
            "last_checked": last_checked_iso,
            "check": check,
            "result": result,
            "latency_ms": latency_ms,
            "reasons": reasons,
        }

        async with httpx.AsyncClient(timeout=self.timeout, headers=headers) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    async def record_event(
        self, type_: str, entity_uid: str | None, payload: dict[str, Any],
    ) -> None:
        """Record an event to Matrix-Hub.

        This method records various types of events such as plans, approvals,
        and rejections to the Matrix-Hub event log.

        Args:
            type_: Event type (e.g., "guardian.plan", "guardian.approve")
            entity_uid: Optional entity UID associated with the event
            payload: Event payload dictionary

        Returns:
            None

        Raises:
            None: Errors are logged as warnings but don't raise exceptions

        Example:
            >>> await client.record_event(
            ...     type_="guardian.plan",
            ...     entity_uid="app-123",
            ...     payload={"plan": {...}, "decision": {...}}
            ... )
        """
        # Determine the appropriate endpoint based on event type
        if type_ == "guardian.approve":
            url = f"{self.base_url}/guardian/approve"
        elif type_ == "guardian.reject":
            url = f"{self.base_url}/guardian/reject"
        else:
            url = f"{self.base_url}/guardian/approve"

        body = payload.copy()

        # Add metadata for plan events
        if type_ == "guardian.plan":
            body["plan_event"] = True
            body["accepted"] = False
            body["plan_id"] = body.get("plan", {}).get("plan_id", "unknown")

        # Ensure entity_uid is in the body
        if entity_uid and "entity_uid" not in body:
            body["entity_uid"] = entity_uid

        async with httpx.AsyncClient(timeout=self.timeout, headers=_auth_headers()) as client:
            resp = await client.post(url, json=body)
            if resp.status_code not in (200, 201, 202):
                logger.warning(
                    "record_event(%s) unexpected status=%s body=%s",
                    type_,
                    resp.status_code,
                    resp.text,
                )


__all__ = ["MatrixHubClient"]
