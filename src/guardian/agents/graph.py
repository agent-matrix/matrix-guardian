from __future__ import annotations

import logging
from typing import Any, Dict, Optional
from datetime import datetime, timezone

from ..services.matrix_ai_client import MatrixAIClient
from ..services.matrix_hub_client import MatrixHubClient
from .policy import Policy, PolicyDecision

logger = logging.getLogger(__name__)


class AutopilotGraph:
    """
    A pragmatic 'graph' that wires nodes procedurally (LangGraph can be slotted later).
    Nodes:
      - choose_targets (done in orchestrator)
      - probe_health (optional/lightweight – out of scope here; use Hub data)
      - plan (via matrix-ai)
      - policy_gate (Policy)
      - record (events and status to Hub)
    """

    def __init__(self, hub_client: MatrixHubClient, ai_client: MatrixAIClient, policy: Policy):
        self.hub = hub_client
        self.ai = ai_client
        self.policy = policy

    async def evaluate_app(self, app: Dict[str, Any]) -> Dict[str, Any]:
        uid = app.get("uid")
        health = app.get("health") or {}
        score = health.get("score")
        status = (health.get("status") or "unknown").lower()

        # Only act if unhealthy or unknown
        actionable = status not in ("ok", "healthy") or (isinstance(score, (int, float)) and score < 0.9)
        if not actionable:
            logger.debug("App %s looks healthy (status=%s, score=%s). Skipping.", uid, status, score)
            return {"uid": uid, "skipped": True, "reason": "healthy"}

        # Build plan context
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

        plan = await self.ai.plan(context=context, constraints=constraints)
        decision: PolicyDecision = self.policy.decide(plan)

        # Always persist the plan as an event
        await self.hub.record_event(
            type_="guardian.plan",
            entity_uid=uid,
            payload={
                "plan": plan,
                "decision": decision.model_dump(),
                "ts": datetime.now(timezone.utc).isoformat(),
            },
        )

        # Optionally auto-approve if policy allows
        if decision.approve and not decision.requires_hitl:
            await self.hub.record_event(
                type_="guardian.approve",
                entity_uid=uid,
                payload={"reason": decision.reason, "ts": datetime.now(timezone.utc).isoformat()},
            )
            action = "auto-approved"
        else:
            action = "hitl-pending"

        return {
            "uid": uid,
            "plan": plan,
            "action": action,
            "decision": decision.model_dump(),
        }
