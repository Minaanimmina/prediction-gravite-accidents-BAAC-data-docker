"""
Modèle SQLAlchemy pour stocker les prédictions en base de données.
"""

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, Integer

from ..utils.database import Base


class Prediction(Base):
    """
    Table pour stocker l'historique des prédictions.
    """

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    features_json = Column(JSON, nullable=False)  # Les features envoyées
    # La gravité prédite (1, 2 ou 3)
    prediction = Column(Integer, nullable=False)
    proba_grav1 = Column(Float, nullable=False)  # Probabilité pour gravité 1
    proba_grav2 = Column(Float, nullable=False)  # Probabilité pour gravité 2
    proba_grav3 = Column(Float, nullable=False)  # Probabilité pour gravité 3

    def __repr__(self) -> str:
        return (
            f"<Prediction(id={self.id}, prediction={self.prediction}, "
            f"timestamp={self.timestamp})>"
        )
