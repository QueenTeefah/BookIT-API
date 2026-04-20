import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_and_get_booking():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create a booking (assuming user already exists & token auth is handled)
        booking_data = {
            "user_id": 1,
            "service_id": 1,
            "date": "2025-12-01",
            "time": "15:00",
            "notes": "Test booking"
        }
        response = await ac.post("/bookings/", json=booking_data)
        assert response.status_code in (201, 200)
        data = response.json()
        assert data["service_id"] == 1
        assert data["notes"] == "Test booking"

        # Get all bookings
        get_response = await ac.get("/bookings/")
        assert get_response.status_code == 200
        bookings = get_response.json()
        assert isinstance(bookings, list)
