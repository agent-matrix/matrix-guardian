"""Autopilot workflow graph execution module.

This module implements the AutopilotGraph class which wires together the
workflow nodes for application evaluation. The graph orchestrates health
checking, plan generation, policy decisions, and event recording.

This is a pragmatic procedural implementation that can be replaced with
LangGraph in the future for more complex workflow requirements.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from ..services.matrix_ai_client import MatrixAIClient
from ..services.matrix_hub_client import MatrixHubClient
from .policy import Policy, PolicyDecision


logger = logging.getLogger(__name__)


class AutopilotGraph:
    """Workflow graph for autopilot application evaluation.

    This class implements a pragmatic workflow graph that wires nodes
    procedurally. It can be replaced with LangGraph for more complex
    workflows in the future.

    Workflow nodes:
    1. choose_targets: Application selection (handled by orchestrator)
    2. probe_health: Optional lightweight probing (uses Hub data)
    3. plan: Remediation plan generation via Matrix-AI
    4. policy_gate: Policy-based decision making
    5. record: Event and status recording to Hub

    Attributes:
        hub: MatrixHub client for data access and event recording
        ai: Matrix-AI client for plan generation
        policy: Policy instance for decision-making

    Example:
        >>> graph = AutopilotGraph(hub_client, ai_client, policy)
        >>> result = await graph.evaluate_app(app_data)
    """

    def __init__(
        self, hub_client: MatrixHubClient, ai_client: MatrixAIClient, policy: Policy,
    ) -> None:
        """Initialize the autopilot workflow graph.

        Args:
            hub_client: Client for MatrixHub API operations
            ai_client: Client for Matrix-AI planning service
            policy: Policy configuration for decision-making
        """
        self.hub = hub_client
        self.ai = ai_client
        self.policy = policy

    async def evaluate_app(self, app: dict[str, Any]) -> dict[str, Any]:
        """Evaluate a single application and determine required actions.

        This method executes the complete workflow for a single application:
        1. Checks health status to determine if action is needed
        2. Generates a remediation plan if unhealthy
        3. Applies policy to determine approval requirements
        4. Records events to MatrixHub for tracking and audit

        Args:
            app: Application dictionary containing at minimum:
                - uid (str): Unique application identifier
                - health (dict): Health status information
                    - status (str): Status string (ok, unhealthy, unknown)
                    - score (float): Health score 0.0-1.0
                - lkg_version (str, optional): Last known good version

        Returns:
            Dict[str, Any]: Evaluation result containing:
                - uid (str): Application identifier
                - skipped (bool, optional): True if app is healthy
                - reason (str, optional): Skip reason if skipped
                - plan (dict, optional): Generated remediation plan
                - action (str): Action taken (auto-approved, hitl-pending)
                - decision (dict): Policy decision details

        Raises:
            Exception: Any errors during evaluation are logged and re-raised

        Example:
            >>> app = {
            ...     "uid": "app-123",
            ...     "health": {"status": "unhealthy", "score": 0.5}
            ... }
            >>> result = await graph.evaluate_app(app)
            >>> print(result["action"])
            'hitl-pending'
        """
        uid = app.get("uid")
        health = app.get("health") or {}
        score = health.get("score")
        status = (health.get("status") or "unknown").lower()

        # Determine if application requires action
        actionable = self._is_actionable(status, score)
        if not actionable:
            logger.debug(
                "App %s looks healthy (status=%s, score=%s). Skipping.", uid, status, score,
            )
            return {"uid": uid, "skipped": True, "reason": "healthy"}

        # Build context for plan generation
        context = {
            "app_id": uid,
            "symptoms": [status] if status else [],
            "lkg": app.get("lkg_version"),
            "observations": {
                "score": score,
                "status": status,
            },
        }
        constraints = {
            "risk": "low",
            "max_steps": 3,
        }

        # Generate remediation plan
        logger.info("Generating remediation plan for unhealthy app %s", uid)
        plan = await self.ai.plan(context=context, constraints=constraints)

        # Apply policy decision
        decision: PolicyDecision = self.policy.decide(plan)
        logger.info(
            "Policy decision for app %s: approve=%s, hitl=%s, reason=%s",
            uid,
            decision.approve,
            decision.requires_hitl,
            decision.reason,
        )

        # Record plan event to Hub
        await self.hub.record_event(
            type_="guardian.plan",
            entity_uid=uid,
            payload={
                "plan": plan,
                "decision": decision.model_dump(),
                "ts": datetime.now(UTC).isoformat(),
            },
        )

        # Handle auto-approval if policy allows
        action: str
        if decision.approve and not decision.requires_hitl:
            await self.hub.record_event(
                type_="guardian.approve",
                entity_uid=uid,
                payload={"reason": decision.reason, "ts": datetime.now(UTC).isoformat()},
            )
            action = "auto-approved"
            logger.info("Plan auto-approved for app %s: %s", uid, decision.reason)
        else:
            action = "hitl-pending"
            logger.info("Plan requires HITL approval for app %s", uid)

        return {
            "uid": uid,
            "plan": plan,
            "action": action,
            "decision": decision.model_dump(),
        }

    def _is_actionable(self, status: str, score: int | float | None) -> bool:
        """Determine if an application requires remediation action.

        Args:
            status: Health status string (ok, healthy, unhealthy, unknown)
            score: Health score between 0.0 and 1.0, or None

        Returns:
            bool: True if application requires action, False if healthy

        Example:
            >>> graph._is_actionable("ok", 0.95)
            False
            >>> graph._is_actionable("unhealthy", 0.5)
            True
        """
        # Skip if explicitly marked as ok or healthy
        if status in ("ok", "healthy"):
            return False

        # Check score threshold if available
        if isinstance(score, (int, float)) and score >= 0.9:
            return False

        # All other cases require action
        return True


__all__ = ["AutopilotGraph"]
