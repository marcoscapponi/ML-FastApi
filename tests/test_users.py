import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_me_unauthenticated(async_client: AsyncClient):
    """Acceso al perfil sin token decuelve 401."""
    response = await async_client.get("/api/v1/users/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_me_authenticated(auth_client: AsyncClient, test_user):
    """El usuario autenticado puede ver su perfil."""
    response = await auth_client.get("/api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["full_name"] == test_user.full_name
    