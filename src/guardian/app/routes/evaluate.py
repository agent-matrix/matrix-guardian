from __future__ import annotations

from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ...risk_profile import evaluate_plan

router = APIRouter()


class EvaluateRequest(BaseModel):
    plan: Dict[str, Any]


@router.post("/v1/evaluate")
async def evaluate(req: EvaluateRequest) -> Dict[str, Any]:
    try:
        return evaluate_plan(req.plan)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
