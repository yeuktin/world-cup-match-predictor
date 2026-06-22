import sys
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from src.database import run_query, save_prediction
from src.predict import predict_match


st.set_page_config(
    page_title="World Cup Match Predictor",
    page_icon="⚽",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: #0b1120;
    color: #f9fafb;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #f9fafb;
    font-weight: 800;
    letter-spacing: -0.04em;
}

p, li, label, div {
    color: #d1d5db;
}

[data-testid="stSidebar"] {
    background-color: #0f172a;
}

.hero-card {
    padding: 2rem;
    border-radius: 0;
    background: #111827;
    
    margin-bottom: 1.5rem;
}

.hero-title {
    font-size: 3rem;
    line-height: 1;
    font-weight: 900;
    color: #f9fafb;
    letter-spacing: -0.06em;
    text-transform: uppercase;
}

.hero-subtitle {
    margin-top: 0.85rem;
    font-size: 1rem;
    color: #d1d5db;
    max-width: 820px;
    line-height: 1.55;
}

.info-card {
    padding: 1.1rem 1.25rem;
    border-radius: 0;
    background: #111827;
    border: 1px solid #243244;
    
    margin-bottom: 1rem;
}

.prediction-card {
    padding: 1.25rem;
    border-radius: 0;
    background: #111827;
    border: 1px solid #243244;
    
    margin-top: 1rem;
}

.winner-card {
    padding: 1.35rem;
    border-radius: 0;
    background: #111827;
    
    text-align: left;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.winner-card h2 {
    color: #f9fafb;
    margin-bottom: 0;
    text-transform: uppercase;
    letter-spacing: -0.04em;
}

[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #243244;
    padding: 1rem;
    border-radius: 0;
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1;
    font-weight: 700;
    text-transform: uppercase;
}

[data-testid="stMetricValue"] {
    color: #f9fafb;
    font-weight: 900;
    letter-spacing: -0.04em;
}

.stButton > button {
    background: #166534;
    color: white;
    border-radius: 0;
    border: 1px solid #166534;
    font-weight: 800;
    padding: 0.8rem 1.5rem;
    width: 100%;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

.stButton > button:hover {
    background: #111827;
    color: white;
    border: 1px solid #111827;
}

div[data-baseweb="select"] > div {
    background-color: #ffffff;
    border-radius: 0;
    border-color: #334155;
}

hr {
    border: none;
    height: 1px;
    background: #243244;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero-card">
    <div class="hero-title">World Cup Match Predictor</div>
    <div class="hero-subtitle">
        Predict international football match outcomes using SQL-backed team data,
        historical performance signals, expected goals, and probability models.
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("How to use this app", expanded=True):
    st.markdown("""
    <div class="info-card">
    <b>Step 1:</b> Select two national teams.<br>
    <b>Step 2:</b> Click <b>Generate Match Prediction</b>.<br>
    <b>Step 3:</b> Review the predicted winner, win probabilities, expected goals, and likely scorelines.<br><br>
    This project is designed as a public portfolio app showing Python, SQL, machine learning,
    data engineering, and interactive dashboard skills.
    </div>
    """, unsafe_allow_html=True)


@st.cache_data
def load_teams():
    return run_query("""
        SELECT
            team_id,
            team_name,
            confederation,
            fifa_rank,
            attack_rating,
            defense_rating,
            midfield_rating,
            form_rating,
            world_cup_group
        FROM teams
        ORDER BY world_cup_group, team_name
    """)


teams_df = load_teams()

if teams_df.empty:
    st.error("No team data found. Run: python3 setup_database.py and python3 upgrade_world_cup_data.py")
    st.stop()

TEAM_PROFILES = {
    "Germany": {"world_cups": 4, "best_player": "Jamal Musiala", "manager": "Julian Nagelsmann", "pedigree": "Historic contender", "note": "Elite tournament history and strong squad depth."},
    "Brazil": {"world_cups": 5, "best_player": "Vinicius Junior", "manager": "Carlo Ancelotti", "pedigree": "World Cup royalty", "note": "High attacking ceiling with elite individual talent."},
    "Argentina": {"world_cups": 3, "best_player": "Lionel Messi", "manager": "Lionel Scaloni", "pedigree": "Defending champion profile", "note": "Elite experience and tournament mentality."},
    "France": {"world_cups": 2, "best_player": "Kylian Mbappe", "manager": "Didier Deschamps", "pedigree": "Modern powerhouse", "note": "Explosive attack and elite tournament consistency."},
    "England": {"world_cups": 1, "best_player": "Jude Bellingham", "manager": "Thomas Tuchel", "pedigree": "High-talent contender", "note": "Deep squad with strong attacking options."},
    "Spain": {"world_cups": 1, "best_player": "Lamine Yamal", "manager": "Luis de la Fuente", "pedigree": "Technical powerhouse", "note": "Possession-heavy team with young star power."},
    "Portugal": {"world_cups": 0, "best_player": "Cristiano Ronaldo", "manager": "Roberto Martinez", "pedigree": "Star-driven contender", "note": "Experienced core with elite attacking talent."},
    "Netherlands": {"world_cups": 0, "best_player": "Virgil van Dijk", "manager": "Ronald Koeman", "pedigree": "Major tournament threat", "note": "Strong defensive structure and transition play."},
    "Canada": {"world_cups": 0, "best_player": "Alphonso Davies", "manager": "Jesse Marsch", "pedigree": "Rising host nation", "note": "Athletic, direct, and dangerous in transition."},
    "United States": {"world_cups": 0, "best_player": "Christian Pulisic", "manager": "Mauricio Pochettino", "pedigree": "Host nation contender", "note": "Young, athletic squad with home advantage."},
    "Mexico": {"world_cups": 0, "best_player": "Santiago Gimenez", "manager": "Javier Aguirre", "pedigree": "Experienced host nation", "note": "Strong tournament experience and home support."},
    "Haiti": {"world_cups": 0, "best_player": "Duckens Nazon", "manager": "Sebastien Migne", "pedigree": "Underdog", "note": "Lower-rated side with upset potential."},
}

DEFAULT_PROFILE = {
    "world_cups": 0,
    "best_player": "N/A",
        "pedigree": "Tournament participant",
    "note": "Profile data can be expanded as more squad information becomes available."
}

def calculate_display_strength(row):
    rank_score = max(0, 100 - float(row.get("fifa_rank", 100)))
    strength = (
        0.30 * float(row.get("attack_rating", 0))
        + 0.25 * float(row.get("defense_rating", 0))
        + 0.20 * float(row.get("midfield_rating", 0))
        + 0.15 * rank_score
        + 0.10 * float(row.get("form_rating", 0)) * 10
    )
    return round(strength, 1)



@st.cache_data
def get_team_history_stats(team_name):
    base_query = """
    SELECT
        COUNT(*) AS matches_played,
        SUM(CASE
            WHEN home_team = ? AND home_score > away_score THEN 1
            WHEN away_team = ? AND away_score > home_score THEN 1
            ELSE 0
        END) AS wins,
        SUM(CASE
            WHEN home_team = ? THEN home_score
            WHEN away_team = ? THEN away_score
            ELSE 0
        END) AS goals_for,
        SUM(CASE
            WHEN home_team = ? THEN away_score
            WHEN away_team = ? THEN home_score
            ELSE 0
        END) AS goals_against
    FROM historical_matches
    WHERE home_team = ? OR away_team = ?
    """

    df = run_query(
        base_query,
        (
            team_name, team_name,
            team_name, team_name,
            team_name, team_name,
            team_name, team_name,
        ),
    )

    recent_query = """
    SELECT match_date, home_team, away_team, home_score, away_score, tournament
    FROM historical_matches
    WHERE home_team = ? OR away_team = ?
    ORDER BY match_date DESC
    LIMIT 10
    """

    recent = run_query(recent_query, (team_name, team_name))

    if df.empty or int(df.iloc[0]["matches_played"] or 0) == 0:
        return {
            "matches_played": 0,
            "win_rate": "N/A",
            "goals_for_per_match": "N/A",
            "goals_against_per_match": "N/A",
            "goal_difference_per_match": "N/A",
            "last_10_form": "N/A",
            "most_recent_match": "N/A",
        }

    row = df.iloc[0]
    matches = int(row["matches_played"])
    wins = int(row["wins"] or 0)
    goals_for = int(row["goals_for"] or 0)
    goals_against = int(row["goals_against"] or 0)

    form_results = []
    most_recent_match = "N/A"

    for _, match in recent.iterrows():
        is_home = match["home_team"] == team_name
        team_goals = match["home_score"] if is_home else match["away_score"]
        opp_goals = match["away_score"] if is_home else match["home_score"]
        opponent = match["away_team"] if is_home else match["home_team"]

        if team_goals > opp_goals:
            form_results.append("W")
        elif team_goals < opp_goals:
            form_results.append("L")
        else:
            form_results.append("D")

        if most_recent_match == "N/A":
            most_recent_match = f'{match["match_date"]}: {team_name} {team_goals}-{opp_goals} {opponent}'

    return {
        "matches_played": matches,
        "win_rate": f"{(wins / matches) * 100:.1f}%",
        "goals_for_per_match": f"{goals_for / matches:.2f}",
        "goals_against_per_match": f"{goals_against / matches:.2f}",
        "goal_difference_per_match": f"{(goals_for - goals_against) / matches:+.2f}",
        "last_10_form": " ".join(form_results),
        "most_recent_match": most_recent_match,
    }


team_names = teams_df["team_name"].tolist()

left, right = st.columns(2)

with left:
    st.subheader("Team A")
    team_a = st.selectbox("Choose Team A", team_names, index=0)

with right:
    st.subheader("Team B")
    default_b_index = 1 if len(team_names) > 1 else 0
    team_b = st.selectbox("Choose Team B", team_names, index=default_b_index)

if team_a == team_b:
    st.warning("Choose two different teams to generate a prediction.")
    st.stop()

team_a_row = teams_df[teams_df["team_name"] == team_a].iloc[0]
team_b_row = teams_df[teams_df["team_name"] == team_b].iloc[0]

st.markdown("<hr>", unsafe_allow_html=True)

team_col_1, team_col_2 = st.columns(2)


team_a_strength = calculate_display_strength(team_a_row)
team_b_strength = calculate_display_strength(team_b_row)

team_a_edge = team_a_strength - team_b_strength
team_b_edge = team_b_strength - team_a_strength

team_a_profile = TEAM_PROFILES.get(team_a, DEFAULT_PROFILE)
team_b_profile = TEAM_PROFILES.get(team_b, DEFAULT_PROFILE)

team_a_history = get_team_history_stats(team_a)
team_b_history = get_team_history_stats(team_b)

with team_col_1:
    st.markdown(f"""
    <div class="info-card">
        <h3>{team_a}</h3>
        <p><b>Group:</b> {team_a_row.get("world_cup_group", "N/A")}</p>
        <p><b>Region:</b> {team_a_row.get("confederation", "N/A")}</p>
    </div>
    """, unsafe_allow_html=True)

with team_col_2:
    st.markdown(f"""
    <div class="info-card">
        <h3>{team_b}</h3>
        <p><b>Group:</b> {team_b_row.get("world_cup_group", "N/A")}</p>
        <p><b>Region:</b> {team_b_row.get("confederation", "N/A")}</p>
    </div>
    """, unsafe_allow_html=True)

predict_clicked = st.button("Generate Match Prediction")

if predict_clicked:
    prediction = predict_match(team_a, team_b)
    scorelines = prediction.get('scorelines', [])

    probs = prediction.get("probabilities", prediction)

    team_a_prob = probs.get("team_a_win", probs.get("team_a_win_probability", probs.get("team_a_prob", 0)))
    draw_prob = probs.get("draw", probs.get("draw_probability", probs.get("draw_prob", 0)))
    team_b_prob = probs.get("team_b_win", probs.get("team_b_win_probability", probs.get("team_b_prob", 0)))

    xg_data = prediction.get("expected_goals", {})
    xg_a = xg_data.get("team_a", prediction.get("expected_goals_a", prediction.get("xg_a", 0)))
    xg_b = xg_data.get("team_b", prediction.get("expected_goals_b", prediction.get("xg_b", 0)))

    if team_a_prob > team_b_prob and team_a_prob > draw_prob:
        winner = team_a
    elif team_b_prob > team_a_prob and team_b_prob > draw_prob:
        winner = team_b
    else:
        winner = "Draw"

    save_prediction(team_a, team_b, probs, xg_a, xg_b)

    st.markdown(f"""
    <div class="winner-card">
        <h2>Predicted Result: {winner}</h2>
    </div>
    """, unsafe_allow_html=True)

    metric_1, metric_2, metric_3 = st.columns(3)

    metric_1.metric(f"{team_a} Win", f"{team_a_prob:.1f}%")
    metric_2.metric("Draw", f"{draw_prob:.1f}%")
    metric_3.metric(f"{team_b} Win", f"{team_b_prob:.1f}%")

    st.markdown("### Expected Goals")

    xg_1, xg_2 = st.columns(2)
    xg_1.metric(f"{team_a} xG", f"{xg_a:.2f}")
    xg_2.metric(f"{team_b} xG", f"{xg_b:.2f}")

    st.markdown("### Match Analysis")

    analysis_1, analysis_2 = st.columns(2)

    with analysis_1:
        st.markdown(f"""
        <div class="info-card">
            <h3>{team_a}</h3>
            <p><b>World Cups Won:</b> {team_a_profile["world_cups"]}</p>
            <p><b>Key Player:</b> {team_a_profile["best_player"]}</p>
            <p><b>World Ranking:</b> {int(team_a_row.get("fifa_rank", 0))}</p>
            <p><b>Historical Matches:</b> {team_a_history["matches_played"]}</p>
            <p><b>Historical Win Rate:</b> {team_a_history["win_rate"]}</p>
            <p><b>Goals Scored Per Match:</b> {team_a_history["goals_for_per_match"]}</p>
            <p><b>Goals Allowed Per Match:</b> {team_a_history["goals_against_per_match"]}</p>
            <p><b>Goal Difference Per Match:</b> {team_a_history["goal_difference_per_match"]}</p>
            <p><b>Last 10 Form:</b> {team_a_history["last_10_form"]}</p>
            <p><b>Most Recent Match:</b> {team_a_history["most_recent_match"]}</p>
            <p><b>Overall Team Strength:</b> {team_a_strength} / 100</p>
            <p><b>Matchup Edge:</b> {team_a_edge:+.1f}</p>
        </div>
        """, unsafe_allow_html=True)

    with analysis_2:
        st.markdown(f"""
        <div class="info-card">
            <h3>{team_b}</h3>
            <p><b>World Cups Won:</b> {team_b_profile["world_cups"]}</p>
            <p><b>Key Player:</b> {team_b_profile["best_player"]}</p>
            <p><b>World Ranking:</b> {int(team_b_row.get("fifa_rank", 0))}</p>
            <p><b>Historical Matches:</b> {team_b_history["matches_played"]}</p>
            <p><b>Historical Win Rate:</b> {team_b_history["win_rate"]}</p>
            <p><b>Goals Scored Per Match:</b> {team_b_history["goals_for_per_match"]}</p>
            <p><b>Goals Allowed Per Match:</b> {team_b_history["goals_against_per_match"]}</p>
            <p><b>Goal Difference Per Match:</b> {team_b_history["goal_difference_per_match"]}</p>
            <p><b>Last 10 Form:</b> {team_b_history["last_10_form"]}</p>
            <p><b>Most Recent Match:</b> {team_b_history["most_recent_match"]}</p>
            <p><b>Overall Team Strength:</b> {team_b_strength} / 100</p>
            <p><b>Matchup Edge:</b> {team_b_edge:+.1f}</p>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("### Most Likely Scorelines")

    if isinstance(scorelines, pd.DataFrame):
        scoreline_df = scorelines.copy()
    else:
        scoreline_df = pd.DataFrame(scorelines)

    st.dataframe(scoreline_df, use_container_width=True)

    st.markdown("""
    <div class="prediction-card">
        <b>Portfolio note:</b> Each prediction is saved into the SQLite database,
        so the project demonstrates SQL storage, model output tracking, and an analytics-ready backend.
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("Select two teams and click Generate Match Prediction.")
