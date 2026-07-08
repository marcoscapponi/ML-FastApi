from pydantic import BaseModel, conlist, Field
from datetime import datetime
from typing import Optional, Dict, Any

class PredictionInput(BaseModel):
    features: conlist(float, min_length=4, max_length=4) = Field(...,
                                                            example=[5.1, 3.5, 1.4, 0.2],
                                                            description="4 caracteristicas numericas (largo y ancho del sepalo y petalo)")

class PredictionOutput(BaseModel):
    id: int
    class_name: str | None = None # Nombre de la clase si esta disponible
    predicted_class: int
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    probability: float
    created_at: datetime | None =  None
    input_data: Optional[Dict[str, Any]] = None
    
    model_config = {"from_attributes": True, "populate_by_name": True}