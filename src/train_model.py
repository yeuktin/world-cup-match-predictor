from pathlib import Path
import joblib
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error

from src.database import initialize_database, load_csvs_to_database, DB_PATH
from src.features import build_training_dataset

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)


def train_models():
    if not DB_PATH.exists():
        initialize_database()
        load_csvs_to_database()

    df = build_training_dataset()

    feature_cols = [
        "rank_diff", "attack_diff", "defense_diff", "midfield_diff", "form_diff",
        "team_a_attack", "team_b_attack", "team_a_defense", "team_b_defense"
    ]

    X = df[feature_cols]
    y_result = df["result"]
    y_goals_a = df["team_a_goals"]
    y_goals_b = df["team_b_goals"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_result, test_size=0.25, random_state=42, stratify=y_result if y_result.nunique() > 1 else None
    )

    classifier = RandomForestClassifier(n_estimators=300, random_state=42, class_weight="balanced")
    classifier.fit(X_train, y_train)

    goal_model_a = RandomForestRegressor(n_estimators=300, random_state=42)
    goal_model_b = RandomForestRegressor(n_estimators=300, random_state=42)
    goal_model_a.fit(X, y_goals_a)
    goal_model_b.fit(X, y_goals_b)

    preds = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, preds)

    joblib.dump(classifier, MODEL_DIR / "match_result_model.joblib")
    joblib.dump(goal_model_a, MODEL_DIR / "goals_a_model.joblib")
    joblib.dump(goal_model_b, MODEL_DIR / "goals_b_model.joblib")

    print("Training complete")
    print(f"Rows used: {len(df)}")
    print(f"Result model accuracy on small mock test set: {accuracy:.2f}")
    print("Note: mock data is for  structure, not real betting accuracy.")


if __name__ == "__main__":
    train_models()
