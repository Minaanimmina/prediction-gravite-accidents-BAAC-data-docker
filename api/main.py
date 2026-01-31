from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path

app = FastAPI(title="Accidents Gravité API")

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "best_model_multiclass.joblib"
FEATURES_PATH = BASE_DIR / "models" / "model_features.csv"

model = joblib.load(MODEL_PATH)
model_features = pd.read_csv(FEATURES_PATH)["feature"].tolist()


class PredictRequest(BaseModel):
    # On accepte un dictionnaire de features
    # Exemple JSON : {"vitesse_max_auto_clean": 50, "acc_est_en_agglo": 1, ...}
    features: dict


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    # Créer un DataFrame avec 1 ligne
    X = pd.DataFrame([req.features])

    # Ajouter les features manquantes (si l'utilisateur n'a pas tout fourni)
    for col in model_features:
        if col not in X.columns:
            X[col] = 0

    # Garder uniquement les colonnes attendues et dans le bon ordre
    X = X[model_features]

    # Prédiction
    pred = model.predict(X)[0]

    # Comme le modèle est entraîné sur y_enc (0/1/2), on remonte en 1/2/3
    pred_grav = int(pred) + 1

    # Probabilités (si disponible)
    proba = None
    if hasattr(model, "predict_proba"):
        p = model.predict_proba(X)[0]  # ex: [p0, p1, p2]
        proba = {
            "grav_1": float(p[0]),
            "grav_2": float(p[1]),
            "grav_3": float(p[2])
        }

    return {"prediction": pred_grav, "proba": proba}
