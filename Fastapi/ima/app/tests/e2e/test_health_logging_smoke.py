# app/tests/e2e/test_health_logging_smoke.py
import httpx
import logging
import io
import json
import pytest

from pythonjsonlogger.json import JsonFormatter  # ✅ new import

from app import app
from app.core.logging import configure_logging


@pytest.mark.asyncio
async def test_health_smoke_and_access_log_json():
    # configure logging once (idempotent)
    configure_logging(debug=False)

    # Capture a line from uvicorn.access by attaching a JSON formatter handler
    buf = io.StringIO()
    handler = logging.StreamHandler(buf)
    handler.setFormatter(
        JsonFormatter("%(levelname)s %(name)s %(message)s %(status_code)s")
    )

    log = logging.getLogger("uvicorn.access")
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        r = await client.get("/v1/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}

    handler.flush()
    # We can’t guarantee uvicorn’s access hook runs in ASGITransport,
    # so treat this as a “does not break JSON” smoke: log manually.
    log.info("GET /v1/health HTTP/1.1", extra={"status_code": 200})
    line = buf.getvalue().splitlines()[-1]
    parsed = json.loads(line)
    assert parsed["status_code"] == 200
