"""
Script de entrenamiento del modelo de clasificacion.

Uso:
    python scripts/train_model.py

Variables de entorno opcionales:
    DATABASE_URL: URL de la BD si queremos cargar datos desde PostgreSQL.
    MODEL_PATH: Ruta donde guardar el modelo (por defecto: src/models/artifacts/model.joblib)
    METADATA_PATH: Ruta para metadatos JSON (por defecto: src/models/artifacts/metadata.json)
"""

import json
import os
import logging
import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sqlalchemy import text

from datetime import datetime, timezone
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Rutas por defecto  (relativas a la raiz del proyecto)
DEFAULT_MODEL_PATH = Path("src/models/artifacts/model.joblib")
DEFAULT_METADATA_PATH = Path("src/models/artifacts/metadata.json")

def load_data() -> pd.DataFrame:
    """
    Carga los datos de entrenamiento.
    Puede leer desde CSV o desde la BD segun configuración.
    """
    # Opcion 1: desde CSV Local
    csv_path = Path("data/iris.csv")
    if csv_path.exists():
        logger.info(f"Cargando datos desde CSV: {csv_path}")
        return pd.read_csv(csv_path)
    
    # Opcion 2: desde BD (si DATABASE_URL esta configurada)
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        logger.info(f"Cargando datos desde BD: {database_url}")
        import asyncio
        from sqlalchemy.ext.asyncio import create_async_engine
        async  def _load_from_db():
            engine = create_async_engine(database_url)
            async with engine.connect() as conn:
                result = await conn.execute(text("SELECT * FROM iris_data"))
                rows = result.fetchall()
                columns = result.keys()
            return pd.DataFrame(rows, columns=columns)
        return asyncio.run(_load_from_db()) 
    
    #Opcion 3: desde sklearn (fallback)
    logger.info("Cargando datos desde sklearn (fallback)")
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    return df

def preprocess_data(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, StandardScaler]:
    """
    Preprocesa los datos: separa features y target, divide en train/test y escala.
    Retorna X, y y el scaler ajustado
    """

    if 'target' not in df.columns:
        raise ValueError("El DataFrame debe contener una columna 'target' con las etiquetas.")
    
    X = df.drop(columns=['target']).values
    y = df['target'].values
    
    # Escalar caracteristicas
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler

def train_model(X_train: np.ndarray, y_train: np.ndarray) -> LogisticRegression:
    """
    Entrena un modelo de regresion logistica con los datos de entrenamiento.
    Retorna el modelo entrenado.
    """
    model = LogisticRegression(max_iter=200, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test) -> dict:
    """
    Evalua el modelo con los datos de prueba y retorna un diccionario con las metricas.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    logger.info(f"Accuracy: {accuracy:.4f}")
    return {"accuracy": accuracy,
            "classification_report": report}

def save_model(model, scaler, metadata: dict):
    """
    Guarda el modelo entrenado, el scaler y los metadatos en las rutas configuradas.
    """
    model_path = Path(os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH))
    metadata_path = Path(os.getenv("METADATA_PATH", DEFAULT_METADATA_PATH))

    # Crear directorios si no existen
    model_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar modelo y scaler juntos
    artifacts = {"model": model, "scaler": scaler}
    joblib.dump(artifacts, model_path)
    logger.info(f"Modelo guardado en: {model_path}")

    # Guardar metadatos
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2, default=str)  # default=str para serializar datetime
    logger.info(f"Metadatos guardados en: {metadata_path}")

def main():
    logger.info("Iniciando proceso de entrenamiento del modelo...")

    # 1. Cargar datos
    df = load_data()
    logger.info(f"Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")

    # 2. Preprocesar datos
    X, y, scaler = preprocess_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # 3. Entrenar modelo
    model = train_model(X_train, y_train)

    # 4. Evaluar modelo
    metrics = evaluate_model(model, X_test, y_test)

    # 5. Obtener nombres de las clases
    class_names = None
    if hasattr(load_iris(), 'target_names'):
        class_names = load_iris().target_names.tolist()
    elif hasattr(df, 'target_names'):
        class_names = df.target_names.tolist()
    else:
        class_names = [str(i) for i in model.classes_.tolist()]

    # 6. Guardar modelo y metadatos
    metadata = {
        "model_name": "LogisticRegression",
        "training_date": datetime.now(timezone.utc).isoformat(),
        "dataset_size": len(df),
        "features": list(df.drop(columns=['target']).columns),
        "classes": class_names,
        "metrics": metrics,
        "framework": "scikit-learn",
        "version": "1.0.0" 
    }
    save_model(model, scaler, metadata)

    logger.info("Proceso de entrenamiento completado exitosamente.")

if __name__ == "__main__":
    main()