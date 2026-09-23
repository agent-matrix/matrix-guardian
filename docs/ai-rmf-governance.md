# AI RMF governance profile

Matrix Guardian maps its governance evidence to the NIST AI Risk Management
Framework functions **GOVERN, MAP, MEASURE, MANAGE** and the NIST generative-AI
profile (NIST AI 600-1).

This is an operational crosswalk, not a claim of NIST certification.

The repository pins the mapping to AI RMF 1.0 because that is the published
framework currently used by the project; NIST has announced that AI RMF 1.0 is
being revised, so the mapping is explicitly versioned.

## Policy endpoint

`POST /v1/evaluate`

Input:

```json
{"plan": {"schema_version":"2.0","plan_id":"...","steps":[...]}}
```

Output is a Matrix OS-compatible PolicyGrant plus an auditable `risk_profile`.

## Fail-closed rules

- forbidden governance/secrets/bypass capabilities are denied,
- high/critical risk requires human approval,
- effectful medium-risk work requires sandboxing,
- low-risk explicitly declared capabilities may be allowed,
- absent/unknown capability declarations require human approval.

Guardian authorizes. It never executes.
