# app/tests/integration/test_create_user.py
import httpx
import pytest
from uuid import uuid4

from app import app


@pytest.mark.asyncio
async def test_create_user_ok():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        email = f"alice+{uuid4().hex[:8]}@example.com"  # ← ensure uniqueness per run
        payload = {"email": email, "full_name": "Alice A"}
        r = await client.post("/v1/users", json=payload)
        assert r.status_code == 201, r.text
        data = r.json()
        assert data["email"] == email
        assert data["full_name"] == "Alice A"
        assert "id" in data


@pytest.mark.asyncio
async def test_create_user_conflict_email():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        email = f"bob+{uuid4().hex[:8]}@example.com"  # unique first, then duplicate
        payload = {"email": email, "full_name": None}
        r1 = await client.post("/v1/users", json=payload)
        assert r1.status_code == 201, r1.text
        r2 = await client.post("/v1/users", json=payload)
        assert r2.status_code == 409
        assert r2.json()["detail"] == "email_already_exists"
