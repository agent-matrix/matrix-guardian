"""Matrix Guardian main entrypoint module.

This module serves as the main entrypoint for the Matrix Guardian application
when running with Uvicorn or other ASGI servers. It imports the FastAPI application
instance and can be extended with startup/shutdown logic as needed.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

from .app.api import app


__all__ = ["app"]

# Future startup/shutdown logic can be added here if needed
