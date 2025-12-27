"""Autopilot orchestration and execution module.

This module implements the core Autopilot class that orchestrates automated
infrastructure monitoring and response. The autopilot discovers applications,
performs health checks, generates remediation plans, applies policy decisions,
and records events.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

from ..autopilot_settings import AutopilotSettings
from ..services.matrix_ai_client import MatrixAIClient
from ..services.matrix_hub_client import MatrixHubClient
from .graph import AutopilotGraph
from .policy import Policy


logger = logging.getLogger(__name__)


class Autopilot:
    """Orchestrates automated infrastructure monitoring and remediation.

    The Autopilot class coordinates the following workflow:
    1. Discovery of applications via MatrixHub
    2. Lightweight health probes (optional)
    3. Remediation plan generation via Matrix-AI
    4. Policy-based decision making (HITL vs auto-approve)
    5. Event emission to Hub for tracking and audit

    This class is stateless by design. All durable state is stored in
    MatrixHub's database (events, checks) or the jobs repository.

    Attributes:
        hub: MatrixHub client for application discovery and event recording
        ai: Matrix-AI client for generating remediation plans
        policy: Policy instance for decision-making rules
        settings: Autopilot configuration settings
        graph: AutopilotGraph instance for workflow execution

    Example:
        >>> hub = MatrixHubClient()
        >>> ai = MatrixAIClient()
        >>> policy = Policy.from_yaml("policy.yaml")
        >>> settings = AutopilotSettings()
        >>> autopilot = Autopilot(hub, ai, policy, settings)
        >>> result = await autopilot.run_once()
    """

    def __init__(
        self,
        hub_client: MatrixHubClient,
        ai_client: MatrixAIClient,
        policy: Policy,
        settings: AutopilotSettings,
    ) -> None:
        """Initialize the Autopilot orchestrator.

        Args:
            hub_client: Client for MatrixHub API operations
            ai_client: Client for Matrix-AI planning service
            policy: Policy configuration for decision-making
            settings: Autopilot configuration settings
        """
        self.hub = hub_client
        self.ai = ai_client
        self.policy = policy
        self.settings = settings
        self.graph = AutopilotGraph(hub_client=self.hub, ai_client=self.ai, policy=self.policy)

    async def run_once(self, target_uid: str | None = None) -> dict[str, Any]:
        """Execute a single autopilot evaluation cycle.

        This method performs one complete autopilot cycle:
        - Discovers applications (or uses the provided target)
        - For each unhealthy/interesting app: generates plan, applies policy,
          and records events
        - Returns a summary useful for telemetry and testing

        Args:
            target_uid: Optional specific application UID to evaluate.
                If None, all applications are evaluated.

        Returns:
            Dict[str, Any]: Summary containing:
                - started_at (str): ISO timestamp when cycle started
                - finished_at (str): ISO timestamp when cycle finished
                - count (int): Number of applications evaluated
                - results (List[Dict]): Results for each application

        Raises:
            Exception: Individual app failures are caught and logged,
                but don't halt the overall cycle

        Example:
            >>> result = await autopilot.run_once(target_uid="app-123")
            >>> print(result["count"])
            1
        """
        logger.info("Autopilot run_once started with target_uid=%s", target_uid)
        started_at = datetime.now(UTC)
        results: list[dict[str, Any]] = []

        # Discover applications
        apps: list[dict[str, Any]] = []
        if target_uid:
            app = await self.hub.get_app_or_none(target_uid)
            if app:
                apps = [app]
            else:
                logger.warning("Target app '%s' not found in MatrixHub", target_uid)
        else:
            apps = await self.hub.list_apps(limit=200)

        # Evaluate each application
        for app in apps:
            try:
                result = await self.graph.evaluate_app(app)
                results.append(result)
            except Exception as e:
                logger.exception("Autopilot evaluation failed for app %s: %s", app.get("uid"), e)
                results.append({"uid": app.get("uid"), "error": str(e)})

        finished_at = datetime.now(UTC)
        summary = {
            "started_at": started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "count": len(results),
            "results": results,
        }

        logger.info("Autopilot run_once finished with %d results", len(results))
        return summary

    async def loop_forever(self, stop_event: asyncio.Event) -> None:
        """Run autopilot in a continuous loop until stopped.

        This method runs the autopilot indefinitely, executing cycles at
        the configured interval. It's designed for headless worker processes.
        The loop can be gracefully stopped by setting the stop_event.

        Args:
            stop_event: asyncio.Event that signals when to stop the loop

        Returns:
            None

        Raises:
            Exception: Individual cycle failures are caught and logged,
                but don't halt the loop

        Example:
            >>> stop_event = asyncio.Event()
            >>> task = asyncio.create_task(autopilot.loop_forever(stop_event))
            >>> # ... later ...
            >>> stop_event.set()
            >>> await task
        """
        interval = max(5, self.settings.interval_sec)
        logger.info(
            "Autopilot loop started; interval=%ss safe_mode=%s hitl=%s",
            interval,
            self.settings.safe_mode,
            self.policy.hitl_enabled,
        )

        while not stop_event.is_set():
            try:
                await self.run_once()
            except Exception:
                logger.exception("Autopilot run_once raised an exception")

            # Wait for either the interval or the stop event
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=interval)
            except TimeoutError:
                # Normal case - interval elapsed, continue loop
                pass

        logger.info("Autopilot loop stopped")


__all__ = ["Autopilot"]
