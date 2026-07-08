import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.base import Prediction

@pytest.mark.asyncio
async  def test_predict_unauthenticated(async_client: AsyncClient):
    """Prediccion sin token devuelve 401."""
    response = await async_client.post("/api/v1/predictions/predict",
                                    json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_predict_success(auth_client: AsyncClient, db_session: AsyncSession, test_user):
    """Prediccion exitosa con token valido."""
    response = await auth_client.post("/api/v1/predictions/predict",
                                    json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert response.status_code == 200
    data = response.json()
    assert "predicted_class" in data
    assert "probability" in data
    assert isinstance(data["predicted_class"], int)
    assert 0 <= data["probability"] <= 1
    result = await db_session.execute(select(Prediction).where(Prediction.user_id == test_user.id))
    predictions = result.scalars().all()
    assert len(predictions) == 1
    assert predictions[0].input_data == {"features": [5.1, 3.5, 1.4, 0.2]}

@pytest.mark.asyncio
async def test_predict_invalid_features(auth_client: AsyncClient):
    """Fallo con features de longitud incorrecta."""
    response = await auth_client.post("/api/v1/predictions/predict",
                                    json={"features": [1.0, 2.0]})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_predict_invalid_token(async_client: AsyncClient):
    """Token invalido o expirado devuelve 401."""
    async_client.headers["Authorization"] = "Bearer invalidtoken123"
    response = await async_client.post("/api/v1/predictions/predict",
                                    json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert response.status_code == 401