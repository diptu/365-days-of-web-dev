from app.core.config import settings
from app.core.logging import setup_logging


def test_settings_defaults():
    assert settings.app_name == "IMA"


def test_logging_setup_runs():
    # Just ensure it doesn't crash
    setup_logging()
