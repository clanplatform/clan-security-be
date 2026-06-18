import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_encrypt_unauthorized(client):
    response = await client.post("/api/v1/encryption/encrypt", json={"plaintext": "secret"})
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_algorithms_unauthorized(client):
    response = await client.get("/api/v1/encryption/algorithms")
    assert response.status_code == 403
