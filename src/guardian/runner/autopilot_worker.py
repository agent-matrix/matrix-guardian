"""Autopilot background worker process.

This module provides the entry point for running the autopilot as a
standalone background worker process. It handles signal management for
graceful shutdown and continuously runs autopilot evaluation cycles.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

import asyncio
import logging
import signal
from typing import Any

from ..agents.autopilot import Autopilot
from ..agents.policy import Policy
from ..autopilot_settings import AutopilotSettings
from ..services.matrix_ai_client import MatrixAIClient
from ..services.matrix_hub_client import MatrixHubClient


# Configure basic logging for the worker process
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("autopilot.worker")


async def _main() -> None:
    """Main entry point for the autopilot worker process.

    This function initializes the autopilot system and runs it continuously
    until a shutdown signal is received. It:
    1. Loads autopilot configuration
    2. Initializes clients and policy
    3. Sets up signal handlers for graceful shutdown
    4. Runs the autopilot loop indefinitely

    Returns:
        None

    Raises:
        Exception: Any unhandled exceptions will cause the worker to exit

    Note:
        The worker exits immediately if AUTOPILOT_ENABLED is set to false.
    """
    cfg = AutopilotSettings()

    # Check if autopilot is enabled
    if not cfg.enabled:
        logger.warning("AUTOPILOT_ENABLED is false; exiting worker process")
        return

    logger.info("Autopilot worker starting with configuration:")
    logger.info("  - Interval: %d seconds", cfg.interval_sec)
    logger.info("  - Safe mode: %s", cfg.safe_mode)
    logger.info("  - Policy path: %s", cfg.policy_path)

    # Initialize clients
    hub = MatrixHubClient()
    ai = MatrixAIClient()

    # Load policy from YAML
    policy = Policy.from_yaml(cfg.policy_path)
    policy.safe_mode = cfg.safe_mode

    # Create autopilot instance
    ap = Autopilot(hub_client=hub, ai_client=ai, policy=policy, settings=cfg)

    # Set up graceful shutdown event
    stop_event = asyncio.Event()

    def _signal_handler(*args: Any) -> None:
        """Handle shutdown signals.

        Args:
            *args: Signal handler arguments (unused)

        Returns:
            None
        """
        logger.info("Received shutdown signal, stopping autopilot worker")
        stop_event.set()

    # Register signal handlers for graceful shutdown
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _signal_handler)

    logger.info("Autopilot worker running, press Ctrl+C to stop")

    # Run autopilot loop until stop signal
    await ap.loop_forever(stop_event)

    logger.info("Autopilot worker stopped")


if __name__ == "__main__":
    asyncio.run(_main())
