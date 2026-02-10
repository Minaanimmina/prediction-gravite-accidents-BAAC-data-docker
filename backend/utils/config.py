"""
Configuration centralisée pour le modèle ML de prédiction d'accidents.
Cette configuration contient les features attendues par le modèle
et les chemins vers les ressources du modèle.
"""

from pathlib import Path

# Chemin de base du backend
BASE_DIR = Path(__file__).resolve().parent.parent

# Chemin vers le modèle d'IA entraîné
MODEL_PATH = BASE_DIR / "data" / "models" / "best_model_multiclass.joblib"

# Liste des features que le modèle expect (IMPORTANTE : l'ordre compte)
# Ces features sont utilisées pour :
# 1. Valider les entrées de l'utilisateur
# 2. Remplir les colonnes manquantes avec 0
# 3. Réorganiser les données dans le bon ordre pour le modèle
MODEL_FEATURES = [
    "acc_est_en_agglo",
    "intersection",
    "luminosite",
    "cond_atmo",
    "etat_surface",
    "vitesse_max_auto_clean",
    "nbre_voies_circu",
    "route_rapide",
    "infra_complexe",
    "periode_jour_nuit_bin",
    "saison_Automne",
    "saison_Ete",
    "saison_Hiver",
    "saison_Printemps",
]

# Nombre de classes de prédiction
NUM_CLASSES = 3  # Gravités 1, 2, 3

# Classes de gravité
GRAVITY_CLASSES = {
    0: "Gravité 1",
    1: "Gravité 2",
    2: "Gravité 3",
}
