from __future__ import annotations

import asyncio
import logging
import signal

from ..autopilot_settings import AutopilotSettings
from ..services.matrix_ai_client import MatrixAIClient
from ..services.matrix_hub_client import MatrixHubClient
from ..agents.policy import Policy
from ..agents.autopilot import Autopilot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("autopilot.worker")


async def _main():
    cfg = AutopilotSettings()
    if not cfg.enabled:
        logger.warning("AUTOPILOT_ENABLED is false; exiting.")
        return

    hub = MatrixHubClient()
    ai = MatrixAIClient()
    policy = Policy.from_yaml(cfg.policy_path)
    policy.safe_mode = cfg.safe_mode

    ap = Autopilot(hub_client=hub, ai_client=ai, policy=policy, settings=cfg)

    stop_event = asyncio.Event()

    def _signal(*_):
        logger.info("Received stop signal.")
        stop_event.set()

    loop = asyncio.get_event_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, _signal)

    await ap.loop_forever(stop_event)


if __name__ == "__main__":
    asyncio.run(_main())
