import pytest
import numpy as np
from src.services.prediction_service import predict, load_model
from src.core.config import settings

@pytest.fixture(scope="module", autouse=True)
def setup_model():
    try:
        load_nodel()
    except FileNotFoundError:
        pytest.skip("Modelo no encontrado. Ejecuta 'python scripts/train_model.py' primero." )

def test_predict_returns_valid_types():
    """La prediccion devuelve tipos correctos."""
    pred_class, prob, class_name = predict([5.1, 3.5, 1.4, 0.2])
    assert isinstance(pred_class, int)
    assert isinstance(prob, float)
    assert class_name is None or isinstance(class_name, str)
    assert 0 <= prob <= 1

def test_predict_consistency():
    """La misma entrada siempre produce la misma salida (modelo determinista)."""
    features = [6.0, 3.0, 4.8, 1.8]
    result1 = predict(features)
    result2 = predict(features)
    assert result1 == result2

def test_predict_different_classes():
    """Diferentes entradas producen (posiblemente) diferentes clases."""
    iris_setosa = [5.1, 3.5, 1.4, 0.2]
    iris_versicolor = [6.0, 2.9, 4.5, 1.5]
    class1, _, _ = predict(iris_setosa)
    class2, _, _ = predict(iris_versicolor)
    assert class1 in [0, 1, 2]
    assert class2 in [0, 1, 2]