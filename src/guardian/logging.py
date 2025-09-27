import logging
import sys
import json
import time


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_object = {
            "timestamp": int(time.time() * 1000),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        # Add extra fields if they exist
        if hasattr(record, 'extra'):
            log_object.update(record.extra)
        return json.dumps(log_object, ensure_ascii=False)


def setup_logging(level: str = "INFO"):
    """Configures the root logger to output JSON logs."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers to avoid duplicate logs
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(handler)
