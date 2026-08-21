"""
API Endpoints Integration Tests for PACT Server.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.mongo import db_manager
from app.db.seed import seed_database
from app.agents.a8_admin_gate import a8_admin_gate


@pytest.fixture(autouse=True)
async def setup_test_db():
    await db_manager.connect()
    await seed_database(force=True)
    a8_admin_gate.set_autopilot(enabled=True, timeout_seconds=0.1)


@pytest.mark.asyncio
async def test_api_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_api_pact_ingest():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {"text": "Q|001|7F3K|15223C03Q0|6QR6VFBQ33|7F", "transport": "http"}
        response = await ac.post("/api/v1/pact/ingest", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ("success", "duplicate")


@pytest.mark.asyncio
async def test_api_sms_webhook():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        form_data = {"Body": "Q|002|8M9L|15223C03Q0|6QR6VFBQ33|7F", "From": "+919876543210"}
        response = await ac.post("/api/v1/sms/webhook", data=form_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "received"


@pytest.mark.asyncio
async def test_api_admin_stats():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/admin/stats")
        assert response.status_code == 200
        data = response.json()
        assert "metrics" in data
        assert data["status"] == "operational"


@pytest.mark.asyncio
async def test_api_sms_inbox():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/sms/inbox")
        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
        assert "count" in data
