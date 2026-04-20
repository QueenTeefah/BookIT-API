import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register new user
        register_response = await ac.post(
            "/auth/register",
            json={
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "testpassword"
            },
        )
        assert register_response.status_code == 201
        data = register_response.json()
        assert "email" in data
        assert data["email"] == "testuser@example.com"

        # Login user
        login_response = await ac.post(
            "/auth/login",
            data={
                "username": "testuser@example.com",
                "password": "testpassword"
            },
        )
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
