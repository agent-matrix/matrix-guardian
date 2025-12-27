"""Policy decision engine for autopilot remediation plans.

This module implements risk-based policy decision making for autopilot
remediation plans. It determines whether plans should be auto-approved
or require human-in-the-loop (HITL) approval based on risk levels and
safety settings.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

import enum
import logging
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class RiskLevel(str, enum.Enum):
    """Risk level enumeration for remediation plans.

    Attributes:
        low: Low risk operations (e.g., read-only checks)
        medium: Medium risk operations (e.g., service restarts)
        high: High risk operations (e.g., rollbacks, scaling)
        critical: Critical risk operations (e.g., data migrations)
    """

    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


# Risk level ordering for comparisons
_RISK_ORDER: dict[RiskLevel, int] = {
    RiskLevel.low: 0,
    RiskLevel.medium: 1,
    RiskLevel.high: 2,
    RiskLevel.critical: 3,
}


class PolicyDecision(BaseModel):
    """Policy decision result for a remediation plan.

    Attributes:
        approve: Whether the plan is approved for execution
        requires_hitl: Whether human-in-the-loop approval is required
        reason: Human-readable explanation for the decision
        risk: Assessed risk level of the plan

    Example:
        >>> decision = PolicyDecision(
        ...     approve=True,
        ...     requires_hitl=False,
        ...     reason="Low risk, auto-approved",
        ...     risk=RiskLevel.low
        ... )
    """

    approve: bool = False
    requires_hitl: bool = True
    reason: str = "HITL required by default"
    risk: RiskLevel = RiskLevel.low


class Policy(BaseModel):
    """Risk-based policy for autopilot decision making.

    This class implements a simple risk-based policy that determines whether
    remediation plans should be auto-approved or require human approval.

    The policy evaluates plans based on:
    - safe_mode: When True, never auto-approve (all require HITL)
    - hitl_enabled: Whether to require HITL for plans above threshold
    - risk_max_auto: Maximum risk level that can be auto-approved

    Attributes:
        safe_mode: If True, never auto-approve any plans
        hitl_enabled: If True, require HITL for plans above threshold
        risk_max_auto: Maximum risk level allowed for automatic approval

    Example:
        >>> policy = Policy(
        ...     safe_mode=False,
        ...     hitl_enabled=True,
        ...     risk_max_auto=RiskLevel.low
        ... )
        >>> plan = {"risk": "low", "steps": [...]}
        >>> decision = policy.decide(plan)
    """

    safe_mode: bool = True
    hitl_enabled: bool = True
    risk_max_auto: RiskLevel = RiskLevel.low

    @classmethod
    def from_yaml(cls, path: str | Path) -> Policy:
        """Load policy configuration from a YAML file.

        Args:
            path: Path to the YAML policy configuration file

        Returns:
            Policy: Policy instance with loaded configuration

        Raises:
            Exception: Any errors during YAML loading are caught and logged,
                returning default policy instead

        Example:
            >>> policy = Policy.from_yaml("config/policy.yaml")
            >>> print(policy.safe_mode)
            True
        """
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

    def decide(self, plan: dict[str, Any]) -> PolicyDecision:
        """Make a policy decision for a remediation plan.

        This method evaluates a remediation plan and returns a decision
        about whether it should be auto-approved or require HITL.

        Decision logic:
        1. If safe_mode is True: Always require HITL
        2. If plan risk <= risk_max_auto: Auto-approve
        3. Otherwise: Require HITL

        Args:
            plan: Remediation plan dictionary containing at minimum:
                - risk (str): Risk level (low, medium, high, critical)

        Returns:
            PolicyDecision: Decision with approval status, HITL requirement,
                and explanation

        Example:
            >>> policy = Policy(safe_mode=False, risk_max_auto=RiskLevel.low)
            >>> plan = {"risk": "low", "steps": ["check_health"]}
            >>> decision = policy.decide(plan)
            >>> print(decision.approve)
            True
        """
        raw_risk = (plan or {}).get("risk", "low")
        try:
            risk = RiskLevel(raw_risk)
        except (ValueError, KeyError):
            logger.warning("Invalid risk level '%s' in plan, defaulting to 'low'", raw_risk)
            risk = RiskLevel.low

        # Safe mode: always require HITL
        if self.safe_mode:
            return PolicyDecision(
                approve=False,
                requires_hitl=self.hitl_enabled,
                reason="Safe mode active; HITL required",
                risk=risk,
            )

        # Check if risk is within auto-approval threshold
        if _RISK_ORDER[risk] <= _RISK_ORDER[self.risk_max_auto]:
            return PolicyDecision(
                approve=True,
                requires_hitl=False,
                reason=f"Risk '{risk}' within auto threshold '{self.risk_max_auto}'",
                risk=risk,
            )

        # Risk exceeds threshold: require HITL
        return PolicyDecision(
            approve=False,
            requires_hitl=self.hitl_enabled,
            reason=f"Risk '{risk}' exceeds auto threshold '{self.risk_max_auto}'",
            risk=risk,
        )


__all__ = ["Policy", "PolicyDecision", "RiskLevel"]
