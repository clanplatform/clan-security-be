import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_list_keys_unauthorized(client):
    response = await client.get("/api/v1/keys/")
    assert response.status_code == 403
