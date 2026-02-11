# Contrôleur pour gérer les prédictions
from fastapi import APIRouter
import pandas as pd
import joblib
import logging

from ..utils.database import SessionLocal
from ..models.prediction import Prediction
from ..utils.schemas import PredictionInput, PredictionCreate, PredictionResponse
from ..utils.config import MODEL_PATH, MODEL_FEATURES

# Crée un routeur pour les endpoints de prédiction
router = APIRouter(prefix="/api/predictions", tags=["predictions"])

# Charge le modèle depuis le fichier
model = joblib.load(MODEL_PATH)

# Utilise les features définies dans config.py
model_features = MODEL_FEATURES


# Endpoint pour faire une prédiction
@router.post("/predict")
def predict(req: PredictionInput):
    # Crée un tableau pandas contenant les features envoyées par l'utilisateur
    X = pd.DataFrame([req.features])

    # Ajoute les features manquantes avec une valeur 0
    # si l'utilisateur ne les a pas envoyées
    for col in model_features:
        if col not in X.columns:
            X[col] = 0

    # Garde uniquement les colonnes que le modèle attend, dans le bon ordre
    X = X[model_features]

    # Fait la prédiction avec le modèle
    # pred sera 0, 1 ou 2
    pred = model.predict(X)[0]

    # Convertit la prédiction de 0/1/2 en 1/2/3
    # (car c'est ce que les utilisateurs attendent)
    pred_grav = int(pred) + 1

    # Initialise la variable pour les probabilités
    proba = None
    # Si le modèle peut donner des probabilités (confiance dans sa prédiction)
    if hasattr(model, "predict_proba"):
        # Récupère les probabilités pour chaque classe
        p = model.predict_proba(X)[0]  # ex: [p0, p1, p2]
        # Les convertit en dictionnaire plus lisible
        proba = {
            "grav_1": float(p[0]),
            "grav_2": float(p[1]),
            "grav_3": float(p[2])
        }

    # Enregistrer en BD (optionnel - ne bloque pas si BD indisponible)
    # Étape A : Crée une session BD
    if SessionLocal is not None:
        try:
            db = SessionLocal()

            try:
                # Étape B : Crée une instance Prediction pour enregistrer
                db_prediction = Prediction(
                    features_json=req.features,
                    prediction=pred_grav,
                    proba_grav1=proba["grav_1"] if proba else 0,
                    proba_grav2=proba["grav_2"] if proba else 0,
                    proba_grav3=proba["grav_3"] if proba else 0
                )

                # Étape C : Ajoute à la BD
                db.add(db_prediction)

                # Étape D : Valide
                db.commit()

            finally:
                # Étape E : Ferme la session
                db.close()
        except Exception as e:
            # Si la BD n'est pas accessible, on continue quand même
            # (utile en dev local ou si la BD est down)
            logging.warning(f"Impossible de sauvegarder en BD: {e}")
    else:
        logging.info("Base de données non disponible - prédiction non sauvegardée")

    # Retourne la prédiction et les probabilités au client
    return {"prediction": pred_grav, "proba": proba}


# Endpoint pour récupérer l'historique de toutes les prédictions
@router.get("/history")
def get_history() -> list[PredictionResponse]:
    # Vérifie si la base de données est disponible
    if SessionLocal is None:
        logging.warning("Base de données non disponible - retour d'un historique vide")
        return []
    
    # Crée une session BD
    db = SessionLocal()

    try:
        # Récupère toutes les prédictions depuis la table
        # C'est l'équivalent de : SELECT * FROM predictions
        predictions = db.query(Prediction).all()

        # Convertit explicitement en PredictionResponse (Pydantic)
        return [PredictionResponse.model_validate(p) for p in predictions]

    finally:
        # Ferme la session
        db.close()
