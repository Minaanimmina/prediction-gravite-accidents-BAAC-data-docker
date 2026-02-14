"""Schemas Pydantic pour les entrees/sorties de l'API."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PredictionInput(BaseModel):
    """Schéma pour l'input : les features à prédire"""

    features: dict


class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # Ce qu'on retourne au client quand on lit une prédiction
    id: int
    timestamp: datetime
    features_json: dict
    prediction: int
    proba_grav1: float
    proba_grav2: float
    proba_grav3: float
