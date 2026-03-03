"""Controleur pour gerer les predictions."""

import logging
import time

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException

from ..metrics import (
    db_query_duration_seconds,
    history_requests_total,
    http_errors_total,
    prediction_confidence_histogram,
    predictions_total,
    update_uptime,
)
from ..models.prediction import Prediction
from ..utils.config import MODEL_FEATURES, MODEL_PATH
from ..utils.database import SessionLocal
from ..utils.schemas import PredictionInput, PredictionResponse

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

model = joblib.load(MODEL_PATH)
model_features = MODEL_FEATURES


@router.post("/predict")
def predict(req: PredictionInput) -> dict[str, object]:
    update_uptime()

    try:
        # Prépare les features
        X = pd.DataFrame([req.features])
        for col in model_features:
            if col not in X.columns:
                X[col] = 0
        X = X[model_features]

        # Prédiction
        pred = model.predict(X)[0]
        pred_grav = int(pred) + 1

        # Probabilités
        proba = None
        if hasattr(model, "predict_proba"):
            p = model.predict_proba(X)[0]
            proba = {
                "grav_1": float(p[0]),
                "grav_2": float(p[1]),
                "grav_3": float(p[2]),
            }
            # On observe la probabilité de la classe prédite (confiance du modèle)
            confidence = float(p[pred])
            prediction_confidence_histogram.observe(confidence)

        # Incrémente le counter APRÈS le succès — bonne pratique !
        # Le label correspond à la gravité prédite
        predictions_total.labels(predicted_gravity=str(pred_grav)).inc()

        # Sauvegarde en BD avec mesure de latence
        if SessionLocal is not None:
            try:
                db = SessionLocal()
                try:
                    start = time.time()  # début du chrono BD

                    db_prediction = Prediction(
                        features_json=req.features,
                        prediction=pred_grav,
                        proba_grav1=(proba["grav_1"] if proba else 0.0),
                        proba_grav2=(proba["grav_2"] if proba else 0.0),
                        proba_grav3=(proba["grav_3"] if proba else 0.0),
                    )
                    db.add(db_prediction)
                    db.commit()

                    db_query_duration_seconds.observe(time.time() - start)  # fin chrono

                finally:
                    db.close()
            except Exception as e:
                logging.warning(f"Impossible de sauvegarder en BD: {e}")
                http_errors_total.labels(error_type="server_error").inc()
        else:
            logging.info("Base de données non disponible - prédiction non sauvegardée")

        return {"prediction": pred_grav, "proba": proba}

    except ValueError as e:
        # Erreur de validation des données d'entrée
        http_errors_total.labels(error_type="validation").inc()
        raise HTTPException(status_code=422, detail=str(e))

    except Exception as e:
        # Erreur serveur inattendue
        http_errors_total.labels(error_type="server_error").inc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
def get_history() -> list[PredictionResponse]:
    update_uptime()

    # Incrémente le counter de consultation d'historique
    history_requests_total.inc()

    if SessionLocal is None:
        logging.warning("Base de données non disponible - retour d'un historique vide")
        return []

    db = SessionLocal()
    try:
        start = time.time()
        predictions = db.query(Prediction).all()
        db_query_duration_seconds.observe(time.time() - start)

        return [PredictionResponse.model_validate(p) for p in predictions]

    except Exception as e:
        http_errors_total.labels(error_type="server_error").inc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()