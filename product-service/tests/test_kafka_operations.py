import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from sqlmodel import SQLModel, create_engine, Session
from app.db import get_session

from app.main import app
from app.producer import get_kafka_producer
from app import settings

TEST_DATABASE_URL = "postgresql://saleemakhtar864:YUaiSR4gF5Bj@ep-bold-cell-01190632.us-east-2.aws.neon.tech/asyncapi?sslmode=require"

# Use the correct database connection string for tests
connection_string = TEST_DATABASE_URL.replace("postgresql", "postgresql+psycopg2")

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app=app)
    yield client
    #app.dependency_overrides.clear()

# @pytest.fixture(scope="session", autouse=True)
# def mock_kafka_producer():
#     mock = AsyncMock()
#     # Mock the start method to return a coroutine mock
#     mock.start.return_value = AsyncMock()
#     return mock


async def test_create_product_success(client: TestClient):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 10.0,
        "expiry": "2023-12-31",
        "brand": "Test Brand",
        "weight": 1.0,
        "category_id": 1,
        "sku": "TESTSKU",
        "stock_quantity": 100,
        "reorder_level": 10,
        "meta_title": "Test Meta Title",
        "meta_description": "Test Meta Description",
        "meta_keywords": "test product"
    }

    response = await client.post("/products", json=product_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"

# @pytest.mark.asyncio
# async def test_create_product_missing_fields(client: TestClient, mock_kafka_producer):
#     product_data = {
#         "description": "Test Description",
#         "expiry": "2023-12-31",
#         "brand": "Test Brand",
#         "weight": 1.0,
#         "category_id": 1,
#         "sku": "TESTSKU",
#         "stock_quantity": 100,
#         "reorder_level": 10,
#         "meta_title": "Test Meta Title",
#         "meta_description": "Test Meta Description",
#         "meta_keywords": "test,product"
#     }

#     response = await client.post("/products", json=product_data)
#     assert response.status_code == 422
#     assert "name" in response.json()["detail"][0]["loc"]
#     assert "price" in response.json()["detail"][1]["loc"]
