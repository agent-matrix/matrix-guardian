from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import httpx
from tenacity import retry, wait_exponential, stop_after_attempt

from ..config import settings

logger = logging.getLogger(__name__)


class MatrixAIClient:
    """
    Thin async client for matrix-ai (/v1/plan).
    """

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[float] = None):
        self.base_url = (base_url or str(settings.MATRIX_AI_BASE)).rstrip("/")
        self.timeout = timeout or float(settings.HTTP_TIMEOUT_SECONDS)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    async def plan(self, context: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/plan"
        payload = {
            "mode": "plan",
            "context": context,
            "constraints": constraints,
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            # Basic schema guard
            for key in ("plan_id", "steps", "risk", "explanation"):
                if key not in data:
                    raise ValueError(f"matrix-ai invalid response missing '{key}'")
            return data
