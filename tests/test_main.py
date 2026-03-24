from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.database import get_session
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def override_get_session() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_list_products_starts_empty(client: TestClient) -> None:
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == []


def test_create_product(client: TestClient) -> None:
    payload = {
        "name": "Sony WH-1000XM5",
        "store": "KSP",
        "product_url": "https://example.com/products/sony-wh1000xm5",
        "current_price": 1299.9,
        "target_price": 999.9,
        "currency": "ILS",
        "is_active": True,
    }

    response = client.post("/products", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == payload["name"]
    assert data["target_price"] == payload["target_price"]


def test_update_product(client: TestClient) -> None:
    create_response = client.post(
        "/products",
        json={
            "name": "Ninja Air Fryer",
            "store": "Amazon",
            "product_url": "https://example.com/products/ninja-air-fryer",
            "current_price": 499.0,
            "target_price": 420.0,
            "currency": "ILS",
            "is_active": True,
        },
    )
    product_id = create_response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={"current_price": 450.0, "target_price": 399.0, "is_active": False},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["current_price"] == 450.0
    assert data["target_price"] == 399.0
    assert data["is_active"] is False


def test_delete_product(client: TestClient) -> None:
    create_response = client.post(
        "/products",
        json={
            "name": "Apple Watch SE",
            "store": "iDigital",
            "product_url": "https://example.com/products/apple-watch-se",
            "current_price": 1049.0,
            "target_price": 899.0,
            "currency": "ILS",
            "is_active": True,
        },
    )
    product_id = create_response.json()["id"]

    delete_response = client.delete(f"/products/{product_id}")
    get_response = client.get(f"/products/{product_id}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_get_product_returns_404_when_missing(client: TestClient) -> None:
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_update_product_returns_404_when_missing(client: TestClient) -> None:
    response = client.put("/products/999", json={"current_price": 100.0})

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_delete_product_returns_404_when_missing(client: TestClient) -> None:
    response = client.delete("/products/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
