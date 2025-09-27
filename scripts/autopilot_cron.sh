#!/usr/bin/env bash
set -euo pipefail

# Run a single Autopilot iteration (useful for CronJobs/systemd timers)
# Requires AUTOPILOT_API_ENABLED=true on the API container OR run the worker directly.

if [[ "${RUN_WORKER:-}" == "1" ]]; then
  # Spawn headless worker (loop)
  exec python -m guardian.runner.autopilot_worker
else
  # Trigger one-shot via API
  : "${GUARDIAN_BASE:=http://localhost:8000}"
  curl -fsS -X POST "${GUARDIAN_BASE}/autopilot/plan-once"
fi
