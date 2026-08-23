import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine, SessionLocal
from app.db.seed import seed_db

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_db(db)
    db.close()
    yield

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "database" in data

def test_get_categories():
    response = client.get("/api/v1/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 6
    names = [c["name"] for c in data]
    assert "Electronics" in names
    assert "Fashion" in names

def test_get_filters():
    response = client.get("/api/v1/filters")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert "minPrice" in data
    assert "maxPrice" in data

def test_get_products():
    response = client.get("/api/v1/products?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert len(data["products"]) > 0
    assert data["total"] > 0

def test_get_products_category_filter():
    response = client.get("/api/v1/products?category=Electronics")
    assert response.status_code == 200
    data = response.json()
    for p in data["products"]:
        assert p["category"].lower() == "electronics"

def test_get_product_detail():
    response = client.get("/api/v1/products/aerobuds-pro")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "aerobuds-pro"
    assert data["price"] > 0
    assert "image" in data

def test_ai_search_english():
    response = client.post("/api/v1/search", json={"query": "Laptop for coding under 60000"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0
    # Price constraint check
    for r in data["results"][:3]:
        assert r["product"]["price"] <= 65000

def test_ai_search_roman_telugu():
    response = client.post("/api/v1/search", json={"query": "Naku 60k lopu coding laptop kavali"})
    assert response.status_code == 200
    data = response.json()
    assert data["language"] in ["roman_telugu", "telugu", "english"]
    assert len(data["results"]) > 0
    top_product = data["results"][0]["product"]
    assert top_product["category"] == "Electronics"

def test_ai_search_telugu_script():
    response = client.post("/api/v1/search", json={"query": "నాకు 60000 లోపు coding laptop కావాలి"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) > 0

def test_assistant_chat():
    response = client.post(
        "/api/v1/assistant/chat",
        json={"message": "Best earbuds under 5000", "session_id": "test_session_1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert len(data["products"]) > 0

def test_compare_products():
    response = client.post(
        "/api/v1/compare",
        json={"product_ids": ["aerobuds-pro", "sonic-beam"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 2
    assert "comparison" in data

def test_cart_operations():
    session = "test_user_session_99"
    # 1. Add item
    res1 = client.post(f"/api/v1/cart/{session}/items", json={"product_id": "aerobuds-pro", "quantity": 1})
    assert res1.status_code == 200
    cart_data = res1.json()
    assert cart_data["item_count"] >= 1
    assert cart_data["total"] > 0

    # 2. Get cart
    res2 = client.get(f"/api/v1/cart/{session}")
    assert res2.status_code == 200
    assert len(res2.json()["items"]) >= 1

    # 3. Clear cart
    client.delete(f"/api/v1/cart/{session}")
    res3 = client.get(f"/api/v1/cart/{session}")
    assert res3.json()["item_count"] == 0

def test_order_checkout_flow():
    session = "test_user_checkout_88"
    # Add item
    client.post(f"/api/v1/cart/{session}/items", json={"product_id": "aerobuds-pro", "quantity": 2})
    
    order_payload = {
        "session_id": session,
        "address": {
            "full_name": "Ravi Kumar",
            "phone": "+91 9876543210",
            "address_line": "Flat 402, High Tech Towers",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500081"
        },
        "payment_method": "UPI"
    }
    
    resp = client.post("/api/v1/orders", json=order_payload)
    assert resp.status_code == 200
    order = resp.json()
    assert order["demo"] is True
    assert order["status"] == "placed"
    assert len(order["items"]) == 1
    assert order["total"] > 0
