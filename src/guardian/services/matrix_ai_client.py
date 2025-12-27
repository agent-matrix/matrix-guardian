"""Matrix-AI API client for remediation plan generation.

This module provides an async HTTP client for interacting with the Matrix-AI
planning service. It generates remediation plans based on application context
and constraints with automatic retries and response validation.

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


class MatrixAIClient:
    """Async HTTP client for Matrix-AI planning service.

    This thin client provides a simple interface to the Matrix-AI /v1/plan
    endpoint for generating remediation plans. It includes automatic retries
    and response validation.

    Attributes:
        base_url: Base URL for the Matrix-AI API
        timeout: HTTP request timeout in seconds

    Example:
        >>> client = MatrixAIClient()
        >>> plan = await client.plan(
        ...     context={"app_id": "app-123", "symptoms": ["unhealthy"]},
        ...     constraints={"risk": "low", "max_steps": 3}
        ... )
        >>> print(plan["plan_id"])
    """

    def __init__(self, base_url: str | None = None, timeout: float | None = None) -> None:
        """Initialize the Matrix-AI client.

        Args:
            base_url: Optional base URL override. If None, uses
                settings.MATRIX_AI_BASE
            timeout: Optional timeout override in seconds. If None, uses
                settings.HTTP_TIMEOUT_SECONDS
        """
        self.base_url = (base_url or str(settings.MATRIX_AI_BASE)).rstrip("/")
        self.timeout = timeout or float(settings.HTTP_TIMEOUT_SECONDS)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    async def plan(self, context: dict[str, Any], constraints: dict[str, Any]) -> dict[str, Any]:
        """Generate a remediation plan using Matrix-AI.

        This method sends a planning request to the Matrix-AI service with
        application context and constraints. The service returns a structured
        plan with steps, risk assessment, and explanation.

        Args:
            context: Application context dictionary containing:
                - app_id (str): Application identifier
                - symptoms (List[str]): List of observed symptoms
                - observations (dict): Additional observations
                - lkg (str, optional): Last known good version
            constraints: Planning constraints dictionary containing:
                - risk (str): Maximum acceptable risk level
                - max_steps (int): Maximum number of steps in plan

        Returns:
            Dict[str, Any]: Plan dictionary containing:
                - plan_id (str): Unique plan identifier
                - steps (List): List of remediation steps
                - risk (str): Assessed risk level (low, medium, high, critical)
                - explanation (str): Human-readable explanation

        Raises:
            httpx.HTTPError: If the HTTP request fails after all retries
            ValueError: If the response is missing required fields

        Example:
            >>> context = {
            ...     "app_id": "app-123",
            ...     "symptoms": ["unhealthy"],
            ...     "observations": {"score": 0.5}
            ... }
            >>> constraints = {"risk": "low", "max_steps": 3}
            >>> plan = await client.plan(context, constraints)
            >>> print(plan["steps"])
            [{"action": "restart", "target": "service"}]
        """
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

            # Validate response schema
            required_fields = ("plan_id", "steps", "risk", "explanation")
            for key in required_fields:
                if key not in data:
                    logger.error("Matrix-AI returned invalid response missing '%s': %s", key, data)
                    raise ValueError(f"matrix-ai invalid response missing '{key}'")

            return data


__all__ = ["MatrixAIClient"]
