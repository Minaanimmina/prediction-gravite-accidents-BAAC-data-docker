from sqlalchemy import Column, Integer, Float, DateTime, JSON
from datetime import datetime
from database import Base


class Prediction(Base):
    __tablename__ = "predictions"
    
    # Identifiant unique (auto-généré)
    id = Column(Integer, primary_key=True)
    
    # Date et heure de la prédiction (auto-généré)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Les features envoyés par l'utilisateur (en JSON)
    features_json = Column(JSON, nullable=False)
    
    # La classe prédite (1, 2 ou 3)
    prediction = Column(Integer, nullable=False)
    
    # Probabilités pour chaque classe
    proba_grav1 = Column(Float, nullable=False)
    proba_grav2 = Column(Float, nullable=False)
    proba_grav3 = Column(Float, nullable=False)