from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import httpx
from tenacity import retry, wait_exponential, stop_after_attempt

from ..config import settings

logger = logging.getLogger(__name__)


def _auth_headers() -> Dict[str, str]:
    headers: Dict[str, str] = {}
    if settings.API_TOKEN:
        headers["Authorization"] = f"Bearer {settings.API_TOKEN}"
    return headers


class MatrixHubClient:
    """
    Async client for Matrix-Hub additive APIs (Stage-1/2).
    """

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[float] = None):
        self.base_url = (base_url or str(settings.MATRIXHUB_API_BASE)).rstrip("/")
        self.timeout = timeout or float(settings.HTTP_TIMEOUT_SECONDS)

    async def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=self.timeout, headers=_auth_headers())

    # ---------- Read ----------
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    async def list_apps(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/apps"
        async with httpx.AsyncClient(timeout=self.timeout, headers=_auth_headers()) as client:
            resp = await client.get(url, params={"limit": limit, "offset": offset})
            resp.raise_for_status()
            data = resp.json() or {}
            return data.get("items", [])

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    async def get_app_or_none(self, uid: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/apps/{uid}"
        async with httpx.AsyncClient(timeout=self.timeout, headers=_auth_headers()) as client:
            resp = await client.get(url)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()

    # ---------- Write ----------
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    async def upsert_status(
        self,
        entity_uid: str,
        score: Optional[float],
        status: Optional[str],
        last_checked_iso: Optional[str],
        check: Optional[str],
        result: Optional[str],
        latency_ms: Optional[float],
        reasons: Optional[dict] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
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
    async def record_event(self, type_: str, entity_uid: Optional[str], payload: Dict[str, Any]) -> None:
        url = f"{self.base_url}/guardian/approve" if type_ == "guardian.approve" else \
              f"{self.base_url}/guardian/reject" if type_ == "guardian.reject" else \
              f"{self.base_url}/guardian/approve"

        body = payload.copy()
        if type_ == "guardian.plan":
            body["plan_event"] = True
            body["accepted"] = False
            body["plan_id"] = body.get("plan", {}).get("plan_id", "unknown")
        if entity_uid and "entity_uid" not in body:
            body["entity_uid"] = entity_uid

        async with httpx.AsyncClient(timeout=self.timeout, headers=_auth_headers()) as client:
            resp = await client.post(url, json=body)
            if resp.status_code not in (200, 201, 202):
                logger.warning("record_event(%s) unexpected status=%s body=%s", type_, resp.status_code, resp.text)
