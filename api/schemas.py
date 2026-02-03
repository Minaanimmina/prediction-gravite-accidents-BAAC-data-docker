from pydantic import BaseModel
from datetime import datetime


class PredictionCreate(BaseModel):
    # Ce qu'on reçoit pour créer une prédiction en BD
    features_json: dict
    prediction: int
    proba_grav1: float
    proba_grav2: float
    proba_grav3: float


class PredictionResponse(BaseModel):
    # Ce qu'on retourne au client quand on lit une prédiction
    id: int
    timestamp: datetime
    features_json: dict
    prediction: int
    proba_grav1: float
    proba_grav2: float
    proba_grav3: float
    
    class Config:
        from_attributes = True