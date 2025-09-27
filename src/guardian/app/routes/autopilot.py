from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Query
from ...autopilot_settings import AutopilotSettings
from ...services.matrix_ai_client import MatrixAIClient
from ...services.matrix_hub_client import MatrixHubClient
from ...agents.policy import Policy
from ...agents.autopilot import Autopilot

router = APIRouter()


@router.get("/autopilot/status")
async def autopilot_status() -> Dict[str, Any]:
    cfg = AutopilotSettings()
    return {
        "enabled": cfg.enabled,
        "api_enabled": cfg.api_enabled,
        "interval_sec": cfg.interval_sec,
        "policy_path": cfg.policy_path,
        "safe_mode": cfg.safe_mode,
    }


@router.post("/autopilot/plan-once")
async def autopilot_plan_once(target_uid: Optional[str] = Query(default=None)) -> Dict[str, Any]:
    cfg = AutopilotSettings()
    if not cfg.api_enabled:
        raise HTTPException(status_code=403, detail="AUTOPILOT_API_ENABLED=false")

    hub = MatrixHubClient()
    ai = MatrixAIClient()
    policy = Policy.from_yaml(cfg.policy_path)
    policy.safe_mode = cfg.safe_mode

    ap = Autopilot(hub_client=hub, ai_client=ai, policy=policy, settings=cfg)
    return await ap.run_once(target_uid=target_uid)
