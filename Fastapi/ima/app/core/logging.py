# app/core/logging.py
from __future__ import annotations

import logging
import logging.config
from typing import Any, Dict

# ✅ Import the new class directly (no DeprecationWarning)
from pythonjsonlogger.json import JsonFormatter


def _dict_config(level: str = "INFO") -> Dict[str, Any]:
    """
    Logging config using JSON for both app logs and uvicorn access logs.
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JsonFormatter,  # ✅ direct class, not string path
                "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s "
                "%(module)s %(funcName)s %(lineno)d",
            },
            "access": {
                "()": JsonFormatter,  # ✅ direct class, not string path
                "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s "
                "%(client_addr)s %(request_line)s %(status_code)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "json",
                "stream": "ext://sys.stdout",
            },
            "access_console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "access",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "app": {"handlers": ["console"], "level": level, "propagate": False},
            "uvicorn": {"handlers": ["console"], "level": level, "propagate": False},
            "uvicorn.error": {
                "handlers": ["console"],
                "level": level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["access_console"],
                "level": level,
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
        },
        "root": {"handlers": ["console"], "level": level},
    }


def configure_logging(debug: bool = False) -> None:
    """
    Apply JSON logging across the app and uvicorn.
    """
    level = "DEBUG" if debug else "INFO"
    logging.config.dictConfig(_dict_config(level=level))
    logging.getLogger("app").debug(
        "Structured logging configured", extra={"debug": debug}
    )
