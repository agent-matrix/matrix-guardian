"""HTTP health probe tool for application monitoring.

This module provides a safe HTTP GET probe function with automatic retries
and timeout handling. It's used by the autopilot system to verify application
health and measure response latency.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

import time
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
async def _fetch(url: str, timeout: float) -> httpx.Response:
    """Internal helper to fetch URL with retries.

    This function is wrapped with tenacity retry decorator to automatically
    retry failed requests up to 3 times with exponential backoff.

    Args:
        url: Target URL to fetch
        timeout: Request timeout in seconds

    Returns:
        httpx.Response: HTTP response object

    Raises:
        httpx.HTTPError: If request fails after all retries
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        return await client.get(url)


async def http_probe(url: str, timeout: float = 5.0) -> dict[str, Any]:
    """Execute a safe HTTP GET probe with automatic retries.

    This function performs an HTTP GET request to the specified URL with
    automatic retry logic and comprehensive error handling. It measures
    response time and returns structured results.

    Args:
        url: Target URL to probe (must be a valid HTTP/HTTPS URL)
        timeout: Request timeout in seconds. Defaults to 5.0 seconds.

    Returns:
        Dict[str, Any]: Probe result containing:
            - ok (bool): True if status code is 2xx or 3xx
            - status_code (int|None): HTTP status code, or None on error
            - latency_ms (float): Response time in milliseconds
            - error (str|None): Error message if request failed, otherwise None

    Raises:
        None: All exceptions are caught and returned in the error field

    Example:
        >>> result = await http_probe("https://example.com")
        >>> print(result)
        {
            "ok": True,
            "status_code": 200,
            "latency_ms": 45.2,
            "error": None
        }

        >>> result = await http_probe("https://invalid-domain.example")
        >>> print(result)
        {
            "ok": False,
            "status_code": None,
            "latency_ms": 1234.5,
            "error": "Connection failed: ..."
        }
    """
    t0 = time.perf_counter()

    try:
        resp = await _fetch(url, timeout=timeout)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "ok": 200 <= resp.status_code < 400,
            "status_code": resp.status_code,
            "latency_ms": latency_ms,
            "error": None,
        }
    except Exception as e:
        latency_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "ok": False,
            "status_code": None,
            "latency_ms": latency_ms,
            "error": str(e),
        }


__all__ = ["http_probe"]
