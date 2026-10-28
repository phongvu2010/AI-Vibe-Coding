import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_get_user(client: AsyncClient):
    # 1. Tạo user mới
    payload = {
        "email": "test_engineer@vibe.dev",
        "full_name": "Test Engineer",
        "is_active": True
    }
    create_res = await client.post("/api/v1/users", json=payload)
    assert create_res.status_code == 201
    user_data = create_res.json()
    assert user_data["email"] == payload["email"]
    assert user_data["full_name"] == payload["full_name"]
    assert "id" in user_data

    user_id = user_data["id"]

    # 2. Lấy thông tin user theo ID
    get_res = await client.get(f"/api/v1/users/{user_id}")
    assert get_res.status_code == 200
    fetched_data = get_res.json()
    assert fetched_data["id"] == user_id
    assert fetched_data["email"] == payload["email"]

@pytest.mark.asyncio
async def test_duplicate_email_error(client: AsyncClient):
    payload = {
        "email": "duplicate@vibe.dev",
        "full_name": "Duplicate User",
        "is_active": True
    }
    res1 = await client.post("/api/v1/users", json=payload)
    assert res1.status_code == 201

    # Thử tạo lại với email trùng
    res2 = await client.post("/api/v1/users", json=payload)
    assert res2.status_code == 400
    assert "detail" in res2.json()


@pytest.mark.asyncio
async def test_list_users(client: AsyncClient):
    res = await client.get("/api/v1/users")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


@pytest.mark.asyncio
async def test_get_nonexistent_user(client: AsyncClient):
    import uuid
    random_id = uuid.uuid4()
    res = await client.get(f"/api/v1/users/{random_id}")
    assert res.status_code == 404
