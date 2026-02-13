"""Application Streamlit pour la prediction de gravite."""

import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000") + "/api/predictions/predict"

st.set_page_config(
    page_title="Gravité des accidents • Prédiction",
    page_icon="🚗",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:'
               'wght@500;600;700&family=Space+Mono:wght@400;700&display'
               '=swap');
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:'
               'wght@400;500;600;700&display=swap');

    :root {
        --bg: #fdfdf8;
        --panel: #fdfdf8;
        --border: #d3d2ca;

        --text: #1f2937;
        --muted: #6b7280;

        --accent: #c15f3c;
        --accent-hover: #a94b2a;

        /* Dropdown */
        --dropdown-bg: #fffdf8;
        --dropdown-hover: #f3e6d8;
        --dropdown-selected: #f4e2cf;

        /* JSON */
        --json-bg: #fffdf8;
        --json-border: #d3d2ca;
    }

    html, body, [data-testid="stAppViewContainer"], .main {
        background: var(--bg) !important;
    }

    /* Polices + couleur par défaut */
    html, body, .stApp {
        font-family: 'DM Sans', system-ui, -apple-system,
                     BlinkMacSystemFont, sans-serif;
        color: var(--text);
    }

    h1, h2, h3, h4, h5 {
        font-family: 'Space Grotesk', system-ui, sans-serif !important;
        letter-spacing: -0.015em;
        color: var(--text);
    }

    p, div, span, label, li,
    input, select, textarea,
    button {
        font-family: 'DM Sans', system-ui, sans-serif !important;
        color: var(--text);
    }

    pre, code,
    [data-testid="stJson"],
    [data-testid="stCodeBlock"],
    .monaco-editor,
    .monaco-editor * {
        font-family: 'Space Mono', monospace !important;
        font-size: 0.9rem;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.4rem;
        max-width: 1480px;
    }

    [data-testid="stSidebar"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"] {
        display: none;
    }

    h1 { font-size: 2.35rem; letter-spacing: -0.02em; margin-bottom: 0.35rem; }
    h2 { font-size: 1.6rem; letter-spacing: -0.01em; }
    h3 { font-size: 1.25rem; margin-bottom: 0.35rem; }
    p { line-height: 1.6; }

    .hero {
        background: #fafaf6;
        border: 1px solid #aeaea6;
        padding: 1.6rem 1.8rem;
        border-radius: 18px;
        box-shadow: none;
        margin-bottom: 1.2rem;
    }

    .card {
        background: var(--panel);
        border: 1px solid var(--border);
        padding: 1.2rem 1.4rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        box-shadow: none;
    }

    .card-muted { color: var(--muted) !important; font-size: 0.95rem; }

    .pill {
        display: inline-block;
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        background: #f0f0ec;
        border: 1px solid #aeaea6;
        color: var(--text);
        font-size: 0.8rem;
        margin-right: 0.4rem;
    }


    /* =========================
       Boutons (st.button, st.form_submit_button, etc.)
       ========================= */
    .stButton > button,
    [data-testid="stBaseButton-secondaryFormSubmit"],
    [data-testid="stBaseButton-primary"],
    [data-testid="stBaseButton-secondary"] {
        background: var(--accent) !important;
        border: none !important;
        padding: 0.6rem 1.1rem !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }

    /* Force le texte en blanc */
    .stButton > button,
    .stButton > button *,
    [data-testid="stBaseButton-secondaryFormSubmit"],
    [data-testid="stBaseButton-secondaryFormSubmit"] *,
    [data-testid="stBaseButton-primary"],
    [data-testid="stBaseButton-primary"] *,
    [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-secondary"] * {
        color: #ffffff !important;
    }

    .stButton > button:hover,
    .stButton > button:focus,
    .stButton > button:active,
    [data-testid="stBaseButton-secondaryFormSubmit"]:hover,
    [data-testid="stBaseButton-secondaryFormSubmit"]:focus,
    [data-testid="stBaseButton-secondaryFormSubmit"]:active {
        background: var(--accent-hover) !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* =========================
       Inputs généraux
       ========================= */
    .stTextInput>div>div>input,
    .stSelectbox>div>div,
    .stDateInput>div>div>input,
    .stMultiSelect>div>div {
        background: #fffdf8 !important;
        color: var(--text) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        box-shadow: inset 0 1px 2px rgba(124, 74, 27, 0.08) !important;
    }

    div[data-baseweb="select"] > div {
        background: #fffdf8 !important;
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        box-shadow: none !important;
    }
    div[data-baseweb="select"] span {
        color: var(--text) !important;
        font-weight: 500;
    }


    /* ==========================================================
        Uniformiser tous les titres de champs (labels Streamlit)
    ========================================================== */

    /* Labels */
    label,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p {
    font-size: 1.02rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    line-height: 1.15 !important;
    margin-bottom: 0.25rem !important;
    }

    [data-testid="stWidgetLabel"] {
    margin-bottom: 0.15rem !important;
    }

    [data-testid="stWidgetLabel"] * {
    color: var(--text) !important;
    }

    /* =========================
            Alerts
    ========================= */
    .stAlert {
        background: #fdfdf8 !important;
        border: 1px solid #d3d2ca !important;
        border-radius: 14px !important;
        box-shadow: none;
    }
    .stAlertContainer,
    div[data-testid="stAlert"],
    div[role="alert"] {
        background: #fdfdf8 !important;
        border: none !important;
        border-radius: 14px !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* =========================
       NumberInput : ZERO bordure partout
       ========================= */
    [data-testid="stNumberInput"],
    [data-testid="stNumberInput"] > div,
    [data-testid="stNumberInput"] div[data-testid="stNumberInputContainer"] {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        background: transparent !important;
    }

    [data-testid="stNumberInput"] div[data-baseweb="base-input"],
    [data-testid="stNumberInput"] div[data-baseweb="input"] {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        background: #fffdf8 !important;
        border-radius: 12px !important;
    }

    [data-testid="stNumberInput"] input[data-testid="stNumberInputField"] {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        background: transparent !important;
        color: var(--text) !important;
    }

    [data-testid="stNumberInput"] div[data-baseweb="base-input"]:focus-within,
    [data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within,
    [data-testid="stNumberInput"] input:focus {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stNumberInput"] button[data-testid="stNumberInputStepDown"],
    [data-testid="stNumberInput"] button[data-testid="stNumberInputStepUp"] {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        background: transparent !important;
        color: var(--text) !important;
    }

    /* =========================
       Dropdown ouvert (selectbox)
       ========================= */
    div[data-no-focus-lock="true"] { background: transparent !important; }

    ul[data-testid="stSelectboxVirtualDropdown"] {
        background: var(--dropdown-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        box-shadow: none !important;
        padding: 0.35rem !important;
    }

    ul[data-testid="stSelectboxVirtualDropdown"] > div,
    ul[data-testid="stSelectboxVirtualDropdown"] > div > div,
    ul[data-testid="stSelectboxVirtualDropdown"] > div > div > div {
        background: var(--dropdown-bg) !important;
    }

    ul[data-testid="stSelectboxVirtualDropdown"] li[role="option"] {
        background: var(--dropdown-bg) !important;
        color: var(--text) !important;
        border-radius: 10px !important;
    }

    ul[data-testid="stSelectboxVirtualDropdown"] li[role="option"]:hover {
        background: var(--dropdown-hover) !important;
    }

    ul[data-testid="stSelectboxVirtualDropdown"] \
    li[role="option"][aria-selected="true"] {
        background: var(--dropdown-selected) !important;
    }

    ul[data-testid="stSelectboxVirtualDropdown"] li[role="option"] * {
        color: var(--text) !important;
        background: transparent !important;
    }

    /* =========================
       st.json : fond clair
       ========================= */
    div[data-testid="stJson"] {
        background: var(--json-bg) !important;
        border: 1px solid var(--json-border) !important;
        border-radius: 12px !important;
        padding: 0.6rem 0.75rem !important;
        box-shadow: none !important;
    }

    div[data-testid="stJson"] .react-json-view {
        background: var(--json-bg) !important;
        color: var(--text) !important;
    }

    div[data-testid="stJson"] .object-key,
    div[data-testid="stJson"] .variable-row,
    div[data-testid="stJson"] .brace-row,
    div[data-testid="stJson"] span {
        color: var(--text) !important;
    }

    div[data-testid="stJson"] .variable-value div {
        color: var(--accent-hover) !important;
        font-weight: 600 !important;
    }

    div[data-testid="stJson"] .variable-row {
        border-left: 1px solid var(--border) !important;
    }

    div[data-testid="stJson"] svg {
        color: var(--muted) !important;
    }

    /* =========================
       Compact-field : réduit espace label -> selectbox
       ========================= */
    .compact-field p {
        margin: 0 0 0.15rem 0 !important;
        padding: 0 !important;
        line-height: 1.15 !important;
    }
    .compact-field [data-testid="stSelectbox"] {
        margin-top: -0.35rem !important;
    }
    .compact-field [data-testid="stSelectbox"] > div {
        margin-top: 0 !important;
    }

    /* ==========================================================
       Aligner le début de la colonne gauche avec la carte
       ========================================================== */
    [data-testid="stHorizontalBlock"] > div:first-child
    [data-testid="stVerticalBlock"] > div:first-child {
        margin-top: 1.2rem !important;
    }

    /* ==========================================================
       Bouton "Lancer la prédiction" pleine largeur
       ========================================================== */
    .predict-btn-wrap .stButton {
        width: 100% !important;
    }
    .predict-btn-wrap .stButton > button {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 0.85rem 1.1rem !important;
        border-radius: 12px !important;
        font-size: 1.02rem !important;
        line-height: 1.1 !important;
    }

    /* ==========================================================
    FIX: halo/boîte sombre autour du dropdown (coins extérieurs)
    ========================================================== */

    div[data-no-focus-lock="true"] {
    background: transparent !important;
    box-shadow: none !important;
    outline: none !important;
    border: none !important;
    filter: none !important;
    }

    div[data-no-focus-lock="true"] > div,
    div[data-no-focus-lock="true"] > div > div {
    background: transparent !important;
    box-shadow: none !important;
    outline: none !important;
    border: none !important;
    }

    ul[data-testid="stSelectboxVirtualDropdown"] {
    background: var(--dropdown-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;

    box-shadow: none !important;
    outline: none !important;
    filter: none !important;

    overflow: hidden !important;
    background-clip: padding-box !important;
    }

    ul[data-testid="stSelectboxVirtualDropdown"] > div {
    background: var(--dropdown-bg) !important;
    box-shadow: none !important;
    border: none !important;
    }

    ul[data-testid="stSelectboxVirtualDropdown"] > div > div,
    ul[data-testid="stSelectboxVirtualDropdown"] > div > div > div {
    background: var(--dropdown-bg) !important;
    box-shadow: none !important;
    border: none !important;
    }

    ul[data-testid="stSelectboxVirtualDropdown"],
    ul[data-testid="stSelectboxVirtualDropdown"] * {
    box-shadow: none !important;
    outline: none !important;
    }


    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="pill">Données ouvertes</div>
        <div class="pill">BAAC</div>
        <div class="pill">Prédiction</div>
        <div class="pill">Sécurité routière</div>
        <h1>Prévoir la gravité d'un accident</h1>
        <p class="card-muted">Aidez les décideurs à anticiper les zones
        et contextes à risque en estimant la gravité probable d'un
        accident à partir de ses conditions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def yes_no_to_int(choice: str) -> int:
    return 1 if choice == "Oui" else 0


left_col, right_col = st.columns([2.1, 1], gap="large")

with left_col:
    col_a, col_b = st.columns(2)

    with col_a:
        vitesse = st.number_input(
            "Vitesse maximale autorisée (km/h)",
            min_value=0,
            max_value=150,
            value=50,
        )

        agglo_label = st.selectbox(
            "L'accident a eu lieu en agglomération",
            ["Non", "Oui"],
            index=1,
        )
        intersection_label = st.selectbox(
            "Dans une intersection",
            ["Non", "Oui"],
            index=1,
        )

    with col_b:
        nb_voies = st.number_input(
            "Nombre de voies",
            min_value=0,
            max_value=10,
            value=2,
        )
        luminosite_map = {
            "Plein jour": 1,
            "Crépuscule ou aube": 2,
            "Nuit sans éclairage public": 3,
            "Nuit avec éclairage public non allumé": 4,
            "Nuit avec éclairage public allumé": 5,
        }
        luminosite_label = st.selectbox(
            "Luminosité",
            list(luminosite_map.keys()),
            index=0,
        )

        cond_atmo_map = {
            "Normale": 1,
            "Pluie légère": 2,
            "Pluie forte": 3,
            "Neige / grêle": 4,
            "Brouillard / fumée": 5,
            "Vent fort / tempête": 6,
            "Temps éblouissant": 7,
            "Temps couvert": 8,
            "Autre": 9,
        }
        cond_atmo_label = st.selectbox(
            "Conditions atmosphériques",
            list(cond_atmo_map.keys()),
            index=0,
        )

        etat_surface_map = {
            "Normale": 1,
            "Mouillée": 2,
            "Flaques": 3,
            "Inondée": 4,
            "Enneigée": 5,
            "Boue": 6,
            "Verglacée": 7,
            "Corps gras / huile": 8,
            "Autre": 9,
        }
        etat_surface_label = st.selectbox(
            "État de la surface",
            list(etat_surface_map.keys()),
            index=0,
        )

    st.markdown(
        '<div class="compact-field">'
        "<p><b>Route rapide</b> "
        '<span class="card-muted">(vitesse maximale > 90 km/h)</span>'
        "</p>",
        unsafe_allow_html=True,
    )
    route_rapide_label = st.selectbox(
        "Route rapide",
        ["Non", "Oui"],
        index=0,
        key="route_rapide",
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="compact-field">'
        "<p><b>Infrastructure complexe</b> "
        '<span class="card-muted">'
        "(intersection, échangeur, plusieurs voies)"
        "</span></p>",
        unsafe_allow_html=True,
    )
    infra_complexe_label = st.selectbox(
        "Infrastructure complexe",
        ["Non", "Oui"],
        index=0,
        key="infra_complexe",
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col_c, col_d = st.columns(2)
    with col_c:
        jour_nuit_label = st.selectbox(
            "L'accident a eu lieu la nuit",
            ["Non", "Oui"],
            index=0,
        )
    with col_d:
        saison = st.selectbox(
            "Saison",
            ["Hiver", "Printemps", "Ete", "Automne"],
            index=0,
        )

    agglo = yes_no_to_int(agglo_label)
    intersection = yes_no_to_int(intersection_label)
    luminosite = luminosite_map[luminosite_label]
    cond_atmo = cond_atmo_map[cond_atmo_label]
    etat_surface = etat_surface_map[etat_surface_label]
    route_rapide = yes_no_to_int(route_rapide_label)
    infra_complexe = yes_no_to_int(infra_complexe_label)
    jour_nuit = yes_no_to_int(jour_nuit_label)

# -------------------------
# Construire le dict features (valeurs attendues par le modèle)
# -------------------------
features = {
    "vitesse_max_auto_clean": vitesse,
    "acc_est_en_agglo": agglo,
    "intersection": intersection,
    "nbre_voies_circu": nb_voies,
    "luminosite": luminosite,
    "cond_atmo": cond_atmo,
    "etat_surface": etat_surface,
    "route_rapide": route_rapide,
    "infra_complexe": infra_complexe,
    "periode_jour_nuit_bin": jour_nuit,
}
for s in ["Hiver", "Printemps", "Ete", "Automne"]:
    features[f"saison_{s}"] = 1 if saison == s else 0

with right_col:
    st.markdown(
        """
        <div class="card">
            <h3>Scénario d'accident</h3>
            <p class="card-muted">Renseignez les conditions de
            circulation et l'environnement pour lancer la
            prédiction.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="predict-btn-wrap">', unsafe_allow_html=True)
    submitted = st.button(
        "Lancer la prédiction",
        key="predict_button",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if "last_prediction" not in st.session_state:
        st.session_state.last_prediction = None
        st.session_state.last_proba = None
        st.session_state.last_error = None

    severity_labels = {
        1: "Blessé léger",
        2: "Blessé hospitalisé",
        3: "Tué",
    }

    if submitted:
        payload = {"features": features}
        try:
            r = requests.post(API_URL, json=payload, timeout=10)
            r.raise_for_status()
            data = r.json()
            st.session_state.last_prediction = data.get("prediction")
            st.session_state.last_proba = data.get("proba")
            st.session_state.last_error = None
        except Exception as exc:
            st.session_state.last_error = str(exc)

    if st.session_state.last_error:
        st.error("L'API ne répond pas correctement.")
        st.caption(f"Détail technique : {st.session_state.last_error}")
        st.info("Vérifie que FastAPI est bien lancé sur le port 8000.")
    elif st.session_state.last_prediction is None:
        st.info("Lance une prédiction pour afficher le résultat ici.")
    else:
        prediction_value = st.session_state.last_prediction
        prediction_label = severity_labels.get(prediction_value, str(prediction_value))

        st.markdown(
            f"""
            <div class="card">
                <h2>{prediction_label}</h2>
                <p class="card-muted">Classe prédite
                (code : {prediction_value}).</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.last_proba:
            st.markdown("### Probabilités par classe")
            st.json(st.session_state.last_proba)

    st.markdown(
        """
        <div class="card">
            <h4>Conseils d'interprétation</h4>
            <ul>
                <li>Comparez les probabilités : plus elles
                sont proches, plus la prédiction est
                incertaine.</li>
                <li>Utilisez la gravité prédite pour
                orienter les actions (prévention, contrôle,
                aménagement).</li>
                <li>Interprétez toujours avec votre contexte
                (lieu, heure, météo) et vos analyses de
                données.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
