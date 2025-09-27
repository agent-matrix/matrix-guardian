from __future__ import annotations

import time
from typing import Any, Dict, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
async def _fetch(url: str, timeout: float) -> httpx.Response:
    async with httpx.AsyncClient(timeout=timeout) as client:
        return await client.get(url)


async def http_probe(url: str, timeout: float = 5.0) -> Dict[str, Any]:
    """
    Safe HTTP GET probe.
    Returns:
      {
        "ok": bool,
        "status_code": int|None,
        "latency_ms": float,
        "error": str|None
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
