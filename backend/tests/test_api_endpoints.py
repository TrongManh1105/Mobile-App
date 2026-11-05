import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_api_health_and_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "healthy"}

        root_resp = await client.get("/")
        assert root_resp.status_code == 200
        assert root_resp.json()["status"] == "online"

@pytest.mark.asyncio
async def test_dishes_and_recommendations_api():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Get dishes
        dishes_resp = await client.get("/api/v1/dishes/")
        assert dishes_resp.status_code == 200
        dishes = dishes_resp.json()
        assert len(dishes) > 0

        # Post recommendations
        rec_payload = {
            "cart_dish_ids": ["pho_01"],
            "current_time_hour": 12,
            "limit": 3
        }
        rec_resp = await client.post("/api/v1/recommendations/dishes", json=rec_payload)
        assert rec_resp.status_code == 200
        recs = rec_resp.json()
        assert len(recs) <= 3
        assert len(recs) > 0

@pytest.mark.asyncio
async def test_poi_api():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        poi_resp = await client.get("/api/v1/poi/nearby?available_wait_minutes=25")
        assert poi_resp.status_code == 200
        pois = poi_resp.json()
        assert isinstance(pois, list)

@pytest.mark.asyncio
async def test_order_creation_and_status_update():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        order_payload = {
            "customer_phone": "0988888888",
            "customer_name": "Trần Thị B",
            "merchant_phone": "0987654321",
            "delivery_type": "DineIn",
            "address_or_table": "Bàn 2",
            "order_notes": "Ít cay",
            "items": [
                {
                    "dish_id": "pho_01",
                    "dish_name": "Phở Bò Tái Nạm",
                    "quantity": 1,
                    "unit_price": 65000,
                    "note": None
                }
            ]
        }
        create_resp = await client.post("/api/v1/orders/", json=order_payload)
        assert create_resp.status_code == 200
        order_data = create_resp.json()
        order_id = order_data["order_id"]
        assert order_data["status"] == "CREATED"
        assert order_data["total_amount"] == 65000
        assert "wa.me" in order_data["whatsapp_url"]

        # Update order status to PREPARING
        status_resp = await client.patch(f"/api/v1/orders/{order_id}/status", json={"status": "PREPARING"})
        assert status_resp.status_code == 200
        assert status_resp.json()["status"] == "PREPARING"

