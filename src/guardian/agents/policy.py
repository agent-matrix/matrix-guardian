from __future__ import annotations

import enum
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class RiskLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


_RISK_ORDER = {
    RiskLevel.low: 0,
    RiskLevel.medium: 1,
    RiskLevel.high: 2,
    RiskLevel.critical: 3,
}


class PolicyDecision(BaseModel):
    approve: bool = False
    requires_hitl: bool = True
    reason: str = "HITL required by default"
    risk: RiskLevel = RiskLevel.low


class Policy(BaseModel):
    """
    Simple risk-based policy:
      - safe_mode: if True, never auto-approve
      - hitl_enabled: if True, require HITL above threshold
      - risk_max_auto: max risk to allow automatic approval
    """
    safe_mode: bool = True
    hitl_enabled: bool = True
    risk_max_auto: RiskLevel = RiskLevel.low

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Policy":
        try:
            data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
            ap = data.get("autopilot", {})
            pol = ap.get("policy", {})
            return cls(
                safe_mode=bool(pol.get("safe_mode", True)),
                hitl_enabled=bool(pol.get("hitl_enabled", True)),
                risk_max_auto=RiskLevel(pol.get("risk_max_auto", "low")),
            )
        except Exception as e:
            logger.warning("Failed to load policy YAML '%s': %s. Using defaults.", path, e)
            return cls()

    def decide(self, plan: Dict[str, Any]) -> PolicyDecision:
        raw_risk = (plan or {}).get("risk", "low")
        try:
            risk = RiskLevel(raw_risk)
        except Exception:
            risk = RiskLevel.low

        if self.safe_mode:
            return PolicyDecision(
                approve=False,
                requires_hitl=self.hitl_enabled,
                reason="Safe mode active; HITL required",
                risk=risk,
            )

        # safe_mode False
        if _RISK_ORDER[risk] <= _RISK_ORDER[self.risk_max_auto]:
            return PolicyDecision(
                approve=True,
                requires_hitl=False,
                reason=f"Risk '{risk}' within auto threshold '{self.risk_max_auto}'",
                risk=risk,
            )

        # Above threshold
        return PolicyDecision(
            approve=False,
            requires_hitl=self.hitl_enabled,
            reason=f"Risk '{risk}' exceeds auto threshold '{self.risk_max_auto}'",
            risk=risk,
        )
