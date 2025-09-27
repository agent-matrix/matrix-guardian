import asyncio
import types
import pytest

from guardian.agents.policy import Policy
from guardian.agents.autopilot import Autopilot
from guardian.autopilot_settings import AutopilotSettings


class _FakeHub:
    async def list_apps(self, limit=100, offset=0):
        return [
            {"uid": "app-ok", "health": {"status": "ok", "score": 0.98}},
            {"uid": "app-bad", "health": {"status": "degraded", "score": 0.5}},
        ]

    async def get_app_or_none(self, uid: str):
        for a in await self.list_apps():
            if a["uid"] == uid:
                return a
        return None

    async def record_event(self, type_, entity_uid, payload):
        return None


class _FakeAI:
    async def plan(self, context, constraints):
        return {"plan_id": "p1", "steps": ["retry"], "risk": "low", "explanation": "test"}


@pytest.mark.asyncio
async def test_autopilot_run_once_smoke():
    hub = _FakeHub()
    ai = _FakeAI()
    policy = Policy(safe_mode=False, hitl_enabled=True, risk_max_auto="low")
    settings = AutopilotSettings(enabled=True, api_enabled=True, interval_sec=1, safe_mode=False)

    ap = Autopilot(hub_client=hub, ai_client=ai, policy=policy, settings=settings)
    out = await ap.run_once()
    assert out["count"] == 2
    actions = {r.get("action") for r in out["results"] if "action" in r}
    assert "auto-approved" in actions or "hitl-pending" in actions
