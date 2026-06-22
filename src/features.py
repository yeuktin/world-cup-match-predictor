import pandas as pd
from src.database import run_query


def get_teams():
    return run_query("SELECT * FROM teams ORDER BY team_name")


def get_players_for_team(team_name: str):
    return run_query(
        "SELECT * FROM players WHERE team_name = ? ORDER BY goals_per_90 DESC",
        (team_name,),
    )


def get_team_stats(team_name: str):
    df = run_query("SELECT * FROM teams WHERE team_name = ?", (team_name,))
    if df.empty:
        raise ValueError(f"Team not found: {team_name}")
    return df.iloc[0]


def build_match_features(team_a: str, team_b: str):
    a = get_team_stats(team_a)
    b = get_team_stats(team_b)

    features = pd.DataFrame([
        {
            "rank_diff": b["fifa_rank"] - a["fifa_rank"],
            "attack_diff": a["attack_rating"] - b["attack_rating"],
            "defense_diff": a["defense_rating"] - b["defense_rating"],
            "midfield_diff": a["midfield_rating"] - b["midfield_rating"],
            "form_diff": a["form_rating"] - b["form_rating"],
            "team_a_attack": a["attack_rating"],
            "team_b_attack": b["attack_rating"],
            "team_a_defense": a["defense_rating"],
            "team_b_defense": b["defense_rating"],
        }
    ])
    return features


def build_training_dataset():
    matches = run_query("SELECT * FROM matches")
    rows = []

    for _, match in matches.iterrows():
        try:
            features = build_match_features(match["team_a"], match["team_b"]).iloc[0].to_dict()
            if match["team_a_goals"] > match["team_b_goals"]:
                result = "team_a_win"
            elif match["team_a_goals"] == match["team_b_goals"]:
                result = "draw"
            else:
                result = "team_b_win"

            features["result"] = result
            features["team_a_goals"] = match["team_a_goals"]
            features["team_b_goals"] = match["team_b_goals"]
            rows.append(features)
        except ValueError:
            continue

    return pd.DataFrame(rows)
