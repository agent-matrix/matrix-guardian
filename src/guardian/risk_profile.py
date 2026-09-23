"""Fail-closed Agent-Matrix plan evaluation.

The output is compatible with Matrix OS PolicyGrant while carrying an auditable
risk profile. Guardian decides permission only; it never executes a plan.
"""
from __future__ import annotations

import hashlib
import time
from typing import Any, Dict, Iterable

RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}

FORBIDDEN_CAPABILITIES = {
    "policy.modify",
    "policy.disable",
    "secrets.read",
    "secrets.export",
    "guardian.bypass",
    "audit.disable",
    "production.direct_write",
}

SANDBOX_PREFIXES = (
    "fs.",
    "shell.",
    "repo.write",
    "code.",
    "package.",
    "infra.plan",
)

HUMAN_PREFIXES = (
    "deploy.",
    "production.",
    "identity.",
    "finance.",
    "model.weights.",
    "routing.policy.",
)


def _steps(plan: Dict[str, Any]) -> list[Dict[str, Any]]:
    raw = plan.get("steps") or []
    return [s for s in raw if isinstance(s, dict)]


def _capabilities(plan: Dict[str, Any]) -> list[str]:
    caps: list[str] = []
    for step in _steps(plan):
        cap = str(step.get("capability") or "").strip()
        if cap and cap not in caps:
            caps.append(cap)
    return caps


def _max_risk(plan: Dict[str, Any]) -> str:
    risks = [str(s.get("risk") or "medium") for s in _steps(plan)]
    if not risks:
        # Legacy plan compatibility.
        risks = [str(plan.get("risk") or "medium")]
    normalized = [r if r in RISK_ORDER else "critical" for r in risks]
    return max(normalized, key=lambda r: RISK_ORDER[r])


def evaluate_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    plan_id = str(plan.get("plan_id") or "")
    if not plan_id:
        raise ValueError("plan_id is required")

    caps = _capabilities(plan)
    risk = _max_risk(plan)
    reasons: list[str] = []

    forbidden = sorted(set(caps) & FORBIDDEN_CAPABILITIES)
    if forbidden:
        decision = "deny"
        reasons.append("forbidden capabilities: " + ", ".join(forbidden))
        allowed: list[str] = []
    elif any(c.startswith(HUMAN_PREFIXES) for c in caps) or risk in {"high", "critical"}:
        decision = "require_human_approval"
        reasons.append(f"risk={risk} or high-impact capability requires human authority")
        allowed = caps
    elif any(c.startswith(SANDBOX_PREFIXES) for c in caps) or risk == "medium":
        decision = "require_sandbox"
        reasons.append(f"risk={risk}; effectful work is sandboxed")
        allowed = caps
    elif caps:
        decision = "allow"
        reasons.append("low-risk known capabilities")
        allowed = caps
    else:
        # Unknown/empty capability sets are fail-closed.
        decision = "require_human_approval"
        reasons.append("plan has no explicit capabilities; fail-closed")
        allowed = []

    seed = f"{plan_id}|{decision}|{'|'.join(caps)}|{risk}|{time.time_ns()}"
    grant_id = "pg_" + hashlib.sha256(seed.encode()).hexdigest()[:20]

    return {
        "grant_id": grant_id,
        "plan_id": plan_id,
        "decision": decision,
        "allowed_capabilities": allowed,
        "expires_at": "",
        "risk_profile": {
            "overall_risk": risk,
            "reasons": reasons,
            "ai_rmf": {
                "profile": "NIST AI RMF 1.0 + NIST AI 600-1 GAI Profile",
                "govern": "policy and authority boundary applied",
                "map": "plan capabilities and impact surface identified",
                "measure": f"highest declared/derived risk={risk}",
                "manage": f"decision={decision}",
            },
        },
    }
