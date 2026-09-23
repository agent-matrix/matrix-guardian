from guardian.risk_profile import evaluate_plan


def plan(capability="repo.read", risk="low"):
    return {
        "schema_version": "2.0",
        "plan_id": "p1",
        "steps": [{
            "step_id": "s1",
            "objective": "x",
            "capability": capability,
            "success_criteria": ["ok"],
            "verifiers": ["check"],
            "risk": risk,
        }],
    }


def test_low_risk_read_is_allowed():
    assert evaluate_plan(plan())["decision"] == "allow"


def test_effectful_work_is_sandboxed():
    assert evaluate_plan(plan("fs.apply_patch", "medium"))["decision"] == "require_sandbox"


def test_forbidden_capability_is_denied():
    assert evaluate_plan(plan("policy.modify", "critical"))["decision"] == "deny"


def test_high_impact_requires_human():
    assert evaluate_plan(plan("deploy.production", "high"))["decision"] == "require_human_approval"


def test_missing_capability_fails_closed():
    p = plan()
    p["steps"][0]["capability"] = ""
    assert evaluate_plan(p)["decision"] == "require_human_approval"
