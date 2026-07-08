import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_tegister_success(async_client: AsyncClient):
    """registro de un nuevo usuario exitoso."""
    response = await async_client.post("/api/v1/auth/register",
                                        json={
                                            "email": "newuser@example.com",
                                            "password": "strongpassword123",
                                            "full_name": "New User"
                                        }) 
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["id"] is not None
    assert "password" not in data

@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient, test_user):
    """Login correcto con credenciales validas."""
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com",
            "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(async_client: AsyncClient, test_user):
    """Login con contrasenia incorrecta."""
    response = await async_client.post("/api/v1/auth/login",
                                    json={"email": "test@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert "incorrectos" in response.json()["detail"].lower()

@pytest.mark.asyncio
async  def test_login_inactive_user(async_client: AsyncClient, db_session: AsyncSession):
    """Un usuario inactivo no puede loguearse."""
    from src.db.base import User
    user = User(email="inactive@example.com",
                hashed_password=hash_password("testpassword"),
                is_active=False)
    db_session.add(user)
    await db_session.commit()
    response = await async_client.post("/api/v1/auth/login",
                                    json={"email": "inactive@example.com", "password": "testpassword"})
    assert response.status_code == 403