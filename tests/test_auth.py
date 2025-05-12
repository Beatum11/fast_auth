import pytest
from httpx import AsyncClient
from src.auth.utils import create_access_token, decode_token
from src.config import settings

@pytest.mark.asyncio
async def test_signup_success(test_app: AsyncClient):
    payload = {
        "name": "John",
        "surname": "Doe",
        "date_of_birth": "2000-01-01",
        "login": "johndoe",
        "email": "john@example.com",
        "password": "securepass"
    }

    response = await test_app.post('/api/v1/auth/signup', json=payload)

    assert response.status_code == 201

#payload without a surname
@pytest.mark.asyncio
async def test_signup_fail(test_app: AsyncClient):
    payload = {
        "name": "John",
        "date_of_birth": "2000-01-01",
        "login": "johndoe",
        "email": "john@example.com",
        "password": "securepass"
    }

    response = await test_app.post('/api/v1/auth/signup', json=payload)

    assert response.status_code == 422



#too short password
@pytest.mark.asyncio
async def test_signup_short_password(test_app: AsyncClient):
    payload = {
        "name": "John",
        "surname": "Doe",
        "date_of_birth": "2000-01-01",
        "login": "johndoe",
        "email": "john@example.com",
        "password": "123"
    }

    response = await test_app.post('/api/v1/auth/signup', json=payload)

    assert response.status_code == 422



@pytest.mark.asyncio
async def test_signin_success(test_app: AsyncClient):
    signup_payload = {
        "name": "John",
        "surname": "Doe",
        "date_of_birth": "2000-01-01",
        "login": "johndoe",
        "email": "john@example.com",
        "password": "securepass"
    }

    await test_app.post("/api/v1/auth/signup", json=signup_payload)

    signin_payload = {
        "email": "john@example.com",
        "password": "securepass"
    }

    response = await test_app.post("/api/v1/auth/signin", json=signin_payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data




@pytest.mark.asyncio
async def test_refresh_success(test_app: AsyncClient):
    signup_payload = {
        "name": "Alice",
        "surname": "Smith",
        "date_of_birth": "1992-03-15",
        "login": "alicesmith",
        "email": "alice@example.com",
        "password": "securepass"
    }

    await test_app.post("/api/v1/auth/signup", json=signup_payload)

    signin_payload = {
        "email": "alice@example.com",
        "password": "securepass"
    }

    signin_response = await test_app.post("/api/v1/auth/signin", json=signin_payload)
    refresh_token = signin_response.json()["refresh_token"]

    headers = {"Authorization": f"Bearer {refresh_token}"}
    response = await test_app.post("/api/v1/auth/refresh", headers=headers)

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_refresh_missing_token(test_app: AsyncClient):
    response = await test_app.post("/api/v1/auth/refresh")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_logout_adds_token_to_blocklist(test_app: AsyncClient, fake_redis_client):
    payload = {"email": "user@example.com", "user_id": "123"}
    access_token = create_access_token(user_data=payload)

    decoded = decode_token(access_token)
    jti = decoded["jti"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = await test_app.post("/api/v1/auth/logout", headers=headers)

    assert response.status_code == 200
    assert response.json()["detail"] == "Logged out"

    assert await fake_redis_client.get(jti) == ""


@pytest.mark.asyncio
async def test_logout_missing_token(test_app: AsyncClient):
    response = await test_app.post("/api/v1/auth/logout")
    assert response.status_code == 403





#NEED TO CHECK IT LATER

# @pytest.mark.asyncio
# async def test_signin_invalid_password(test_app: AsyncClient):
#     signup_payload = {
#         "name": "Jane",
#         "surname": "Doe",
#         "date_of_birth": "1990-01-01",
#         "login": "janedoe",
#         "email": "jane@example.com",
#         "password": "realpassword"
#     }

#     await test_app.post("/api/v1/auth/signup", json=signup_payload)

#     signin_payload = {
#         "email": "jane@example.com",
#         "password": "wrongpassword"
#     }

#     response = await test_app.post("/api/v1/auth/signin", json=signin_payload)

#     assert response.status_code == 401
#     assert response.json()["detail"] == "Invalid email or password"
