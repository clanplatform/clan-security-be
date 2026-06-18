import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_create_dsr_unauthorized(client):
    response = await client.post("/api/v1/data-subject-requests/", json={
        "subject_email": "test@example.com",
        "request_type": "access",
    })
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_dsrs_unauthorized(client):
    response = await client.get("/api/v1/data-subject-requests/")
    assert response.status_code == 403
