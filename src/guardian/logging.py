"""Structured JSON logging configuration module.

This module provides structured JSON logging functionality for the Matrix Guardian
application. It includes a custom JSON formatter and a setup function to configure
the root logger with consistent JSON output format.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

import json
import logging
import sys
import time
from typing import Any


class JsonFormatter(logging.Formatter):
    """Custom logging formatter that outputs structured JSON logs.

    This formatter converts log records into JSON objects with consistent
    structure including timestamp, level, message, and logger name. Any
    extra fields attached to the record are also included.

    Attributes:
        None (inherits from logging.Formatter)

    Example:
        >>> formatter = JsonFormatter()
        >>> handler = logging.StreamHandler()
        >>> handler.setFormatter(formatter)
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON string.

        Args:
            record: The log record to format

        Returns:
            JSON-formatted string representation of the log record

        Example:
            >>> record = logging.LogRecord(...)
            >>> formatter = JsonFormatter()
            >>> json_output = formatter.format(record)
        """
        log_object: dict[str, Any] = {
            "timestamp": int(time.time() * 1000),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }

        # Add extra fields if they exist
        if hasattr(record, "extra"):
            log_object.update(record.extra)

        return json.dumps(log_object, ensure_ascii=False)


def setup_logging(level: str = "INFO") -> None:
    """Configure the root logger to output structured JSON logs.

    This function sets up the root logger with a JSON formatter and stream
    handler that outputs to stdout. It clears any existing handlers to
    avoid duplicate log entries.

    Args:
        level: The logging level to set (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            Defaults to "INFO".

    Returns:
        None

    Raises:
        ValueError: If an invalid logging level is provided

    Example:
        >>> setup_logging("DEBUG")
        >>> logging.info("Application started")
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers to avoid duplicate logs
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(handler)


__all__ = ["JsonFormatter", "setup_logging"]
