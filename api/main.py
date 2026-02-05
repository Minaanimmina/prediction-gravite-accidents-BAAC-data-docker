# Importe les outils nécessaires pour créer l'API
from fastapi import FastAPI
# Pydantic permet de vérifier que les données reçues sont du bon type
from pydantic import BaseModel
# pandas et joblib sont utilisés pour traiter les données et charger le modèle
import pandas as pd
import joblib
from pathlib import Path
# Pour la base de données
from database import SessionLocal, init_db
from models import Prediction
from schemas import PredictionCreate, PredictionResponse

# Crée l'application API FastAPI
app = FastAPI(title="Accidents Gravité API")

# Initialise la BD au démarrage de l'app
# Cela crée la table "predictions" si elle n'existe pas
init_db()

# Définit le chemin de base du projet
# (remonte de deux niveaux depuis ce fichier)
BASE_DIR = Path(__file__).resolve().parent.parent

# Chemin vers le modèle d'IA entraîné
MODEL_PATH = BASE_DIR / "models" / "best_model_multiclass.joblib"
# Chemin vers le fichier qui liste les noms des features (colonnes)
# que le modèle attend
FEATURES_PATH = BASE_DIR / "models" / "model_features.csv"

# Charge le modèle depuis le fichier
model = joblib.load(MODEL_PATH)
# Récupère la liste des noms des features à partir du fichier CSV
model_features = pd.read_csv(FEATURES_PATH)["feature"].tolist()


# Classe qui définit la structure des données attendues lors d'une
# requête de prédiction
class PredictRequest(BaseModel):
    # La requête doit contenir un dictionnaire appelé "features"
    # Exemple : {"vitesse_max_auto_clean": 50, "acc_est_en_agglo": 1, ...}
    features: dict


# Endpoint (point d'accès) pour vérifier que l'API fonctionne
@app.get("/health")
def health():
    # Retourne un message simple indiquant que l'API est en ligne
    return {"status": "ok"}


# Endpoint pour faire une prédiction
@app.post("/predict")
def predict(req: PredictRequest):
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

    # Enregistrer en BD
    # Étape A : Crée une session BD
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

    # Retourne la prédiction et les probabilités au client
    return {"prediction": pred_grav, "proba": proba}


# Endpoint pour récupérer l'historique de toutes les prédictions
@app.get("/history")
def get_history() -> list[PredictionResponse]:
    # Crée une session BD
    db = SessionLocal()

    try:
        # Récupère toutes les prédictions depuis la table
        # C'est l'équivalent de : SELECT * FROM predictions
        predictions = db.query(Prediction).all()

        # Retourne la liste (Pydantic va les convertir en PredictionResponse)
        return predictions

    finally:
        # Ferme la session
        db.close()
