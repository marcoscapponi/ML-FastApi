"""Servicio de prediccion: carga del modelo e inferencia."""

import json
import joblib
import numpy as np
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.db.base import Prediction
from src.schemas.prediction import PredictionInput, PredictionOutput
from src.core.config import settings

model_artifacts = None
metadata = None

def load_model():
    global model_artifacts, metadata
    model_path = Path(settings.MODEL_PATH)
    metadata_path = Path(settings.METADATA_PATH)
    if not model_path.exists():
        raise FileNotFoundError(f"Modelo no encontrado en {model_path}")
    model_artifacts = joblib.load(model_path)
    if metadata_path.exists():
        with open(metadata_path) as f:
            metadata = json.load(f)

def predict(features: list[float]) -> tuple[int, float, str | None]:
    if model_artifacts is None:
        raise RuntimeError("El modelo no ha sido cargado.")
    model = model_artifacts["model"]
    scaler = model_artifacts["scaler"]
    features_array = np.array(features).reshape(1, -1)
    features_scaled = scaler.transform(features_array)
    predicted_class = int(model.predict(features_scaled)[0])
    probabilities = model.predict_proba(features_scaled)[0]
    max_prob = float(np.max(probabilities))
    class_name = None
    if metadata and "classes" in metadata:
        classes = metadata["classes"]
        if predicted_class < len(classes):
            class_name = str(classes[predicted_class])
    return predicted_class, max_prob, class_name

async def create_prediction(db: AsyncSession, user_id: int, input_data: PredictionInput) -> PredictionOutput:
    pred_class, prob, class_name = predict(input_data.features)
    prediction = Prediction(
        user_id=user_id,
        input_data={"features": input_data.features},
        predicted_class=pred_class,
        probability=prob,
        class_names=class_name,
        sepal_length=input_data.features[0],
        sepal_width=input_data.features[1],
        petal_length=input_data.features[2],
        petal_width=input_data.features[3]
    )
    db.add(prediction)
    await db.commit()
    await db.refresh(prediction)
    return PredictionOutput(
        predicted_class=pred_class,
        probability=prob,
        class_name=class_name,
        created_at=prediction.created_at,
        input_data=prediction.input_data,
    )