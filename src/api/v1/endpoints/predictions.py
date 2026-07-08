from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.base import User, Prediction
from src.db.session import get_db
from src.schemas.prediction import PredictionInput, PredictionOutput
from src.api.v1.dependencies import get_current_user
from src.services.prediction_service import create_prediction

router = APIRouter(tags=["predictions"])

@router.post("/predict", response_model=PredictionOutput)
async def predict(
    input_data: PredictionInput,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Realiza una predicción y la almacena en la base de datos."""
    return await create_prediction(db, current_user.id, input_data)

@router.get("/history", response_model=List[PredictionOutput])
async def get_prediction_history(
    current_user: User = Depends(get_current_user),
    limit: int = 10000,
    db: AsyncSession = Depends(get_db)
):
    """Devuelve el historial de predicciones del usuario autenticado."""
    result = await db.execute(
        select(Prediction)
        .where(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .limit(limit)
    )
    predictions = result.scalars().all()

    output = []
    for p in predictions:
        output.append(
            PredictionOutput(
                id=p.id,
                class_name=p.class_name or "",          # corregido: class_name (no class_names)
                predicted_class=p.predicted_class,
                sepal_length=p.sepal_length or 0.0,
                sepal_width=p.sepal_width or 0.0,
                petal_length=p.petal_length or 0.0,
                petal_width=p.petal_width or 0.0,
                probability=p.probability or 0.0,
                created_at=p.created_at,
                input_data=p.input_data
            )
        )
    return output