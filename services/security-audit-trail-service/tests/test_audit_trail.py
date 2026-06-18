import pytest
from unittest.mock import patch


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_create_audit_entry_unauthorized(client):
    response = await client.post("/api/v1/audit-entries/", json={
        "action": "LOGIN", "resource": "/auth/login",
        "service": "auth-service", "result": "SUCCESS",
    })
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_entries_unauthorized(client):
    response = await client.get("/api/v1/audit-entries/")
    assert response.status_code == 403
