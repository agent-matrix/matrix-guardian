from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from ..autopilot_settings import AutopilotSettings
from ..services.matrix_ai_client import MatrixAIClient
from ..services.matrix_hub_client import MatrixHubClient
from .graph import AutopilotGraph
from .policy import Policy

logger = logging.getLogger(__name__)


class Autopilot:
    """
    Autopilot orchestrates:
      1) discovery of apps (via MatrixHub),
      2) lightweight probes (optional),
      3) plan generation (via Matrix-AI),
      4) policy decision (HITL vs auto-approve),
      5) event emission to Hub.

    Stateless by design; any durable state should live in MatrixHub DB (events, checks) or jobs repo.
    """

    def __init__(
        self,
        hub_client: MatrixHubClient,
        ai_client: MatrixAIClient,
        policy: Policy,
        settings: AutopilotSettings,
    ):
        self.hub = hub_client
        self.ai = ai_client
        self.policy = policy
        self.settings = settings
        self.graph = AutopilotGraph(hub_client=self.hub, ai_client=self.ai, policy=self.policy)

    async def run_once(self, target_uid: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a single autopilot cycle:
        - Discover apps or use the provided target
        - For each unhealthy/interesting app: plan + policy + record events
        Returns a summary dict useful for telemetry/tests.
        """
        logger.info("Autopilot run_once started target_uid=%s", target_uid)
        started_at = datetime.now(timezone.utc)
        results: List[Dict[str, Any]] = []

        apps = []
        if target_uid:
            app = await self.hub.get_app_or_none(target_uid)
            if app:
                apps = [app]
            else:
                logger.warning("Target app '%s' not found.", target_uid)
        else:
            apps = await self.hub.list_apps(limit=200)

        for app in apps:
            try:
                r = await self.graph.evaluate_app(app)
                results.append(r)
            except Exception as e:
                logger.exception("Autopilot failed on app %s: %s", app.get("uid"), e)
                results.append({"uid": app.get("uid"), "error": str(e)})

        finished_at = datetime.now(timezone.utc)
        summary = {
            "started_at": started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "count": len(results),
            "results": results,
        }
        logger.info("Autopilot run_once finished with %d results", len(results))
        return summary

    async def loop_forever(self, stop_event: asyncio.Event) -> None:
        """
        Headless worker loop. Stops when `stop_event` is set.
        """
        interval = max(5, self.settings.interval_sec)
        logger.info("Autopilot loop started; interval=%ss safe_mode=%s hitl=%s",
                    interval, self.settings.safe_mode, self.policy.hitl_enabled)
        while not stop_event.is_set():
            try:
                await self.run_once()
            except Exception:
                logger.exception("Autopilot run_once raised")
            await asyncio.wait([stop_event.wait()], timeout=interval)
        logger.info("Autopilot loop stopped.")
