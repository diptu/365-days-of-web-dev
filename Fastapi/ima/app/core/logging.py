# app/core/logging.py
import logging

try:
    # New location (no warning)
    from pythonjsonlogger.json import JsonFormatter
except Exception:
    try:
        # Back-compat for older versions
        from pythonjsonlogger.jsonlogger import JsonFormatter  # deprecated path
    except Exception:
        JsonFormatter = None


def setup_logging() -> None:
    """Configure structured JSON logging; fallback to plain logs."""
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    if JsonFormatter:
        formatter = JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    handler.setFormatter(formatter)
    root.handlers = [handler]
