import pytest

from main import app


@pytest.mark.asyncio
async def test_register(client):
    response = await client.post(
        app.url_path_for("register"),
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_auth(client, test_db):
    await client.post(
        app.url_path_for("register"),
        json={"username": "testuser", "password": "testpassword"}
    )

    response = await client.post(
        app.url_path_for("auth"),
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
