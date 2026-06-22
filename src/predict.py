from pathlib import Path
import math
import joblib
import pandas as pd
from src.features import build_match_features, get_players_for_team
from src.database import save_prediction

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"


def poisson_probability(lmbda, goals):
    return (math.exp(-lmbda) * (lmbda ** goals)) / math.factorial(goals)


def scoreline_probabilities(xg_a, xg_b, max_goals=5):
    rows = []
    for goals_a in range(max_goals + 1):
        for goals_b in range(max_goals + 1):
            prob = poisson_probability(xg_a, goals_a) * poisson_probability(xg_b, goals_b)
            rows.append({
                "scoreline": f"{goals_a}-{goals_b}",
                "team_a_goals": goals_a,
                "team_b_goals": goals_b,
                "probability": prob,
            })
    return pd.DataFrame(rows).sort_values("probability", ascending=False)


def predict_match(team_a: str, team_b: str):
    classifier = joblib.load(MODEL_DIR / "match_result_model.joblib")
    goals_a_model = joblib.load(MODEL_DIR / "goals_a_model.joblib")
    goals_b_model = joblib.load(MODEL_DIR / "goals_b_model.joblib")

    X = build_match_features(team_a, team_b)
    class_probs = classifier.predict_proba(X)[0]
    classes = classifier.classes_

    probs = {"team_a_win": 0.0, "draw": 0.0, "team_b_win": 0.0}
    for label, prob in zip(classes, class_probs):
        probs[label] = float(prob)

    xg_a = max(0.1, float(goals_a_model.predict(X)[0]))
    xg_b = max(0.1, float(goals_b_model.predict(X)[0]))

    scorelines = scoreline_probabilities(xg_a, xg_b).head(8)
    save_prediction(team_a, team_b, probs, xg_a, xg_b)

    return {
        "probabilities": probs,
        "expected_goals_a": xg_a,
        "expected_goals_b": xg_b,
        "scorelines": scorelines,
    }


def player_scoring_probability(player_name: str, team_name: str, team_xg: float):
    players = get_players_for_team(team_name)
    player = players[players["player_name"] == player_name]
    if player.empty:
        return 0.0

    p = player.iloc[0]
    base = float(p["goals_per_90"]) * float(p["starter_rating"])
    team_factor = min(team_xg / 1.5, 1.8)
    probability = 1 - math.exp(-(base * team_factor))
    return min(max(probability, 0), 0.95)
