import sqlite3
from pathlib import Path
import pandas as pd

CSV_PATH = Path("data/external/results.csv")
DB_PATH = Path("database/worldcup.db")

if not CSV_PATH.exists():
    raise FileNotFoundError("Missing data/external/results.csv")

print("Loading CSV...")
df = pd.read_csv(CSV_PATH)

required = [
    "date",
    "home_team",
    "away_team",
    "home_score",
    "away_score",
    "tournament",
    "city",
    "country",
    "neutral"
]

missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Missing columns: {missing}")

df = df[required].copy()

print(f"Found {len(df)} matches")

df["result"] = df.apply(
    lambda row: "Home Win"
    if row["home_score"] > row["away_score"]
    else "Away Win"
    if row["home_score"] < row["away_score"]
    else "Draw",
    axis=1
)

df["total_goals"] = df["home_score"] + df["away_score"]
df["neutral"] = df["neutral"].astype(int)

df = df.rename(columns={
    "date": "match_date"
})

conn = sqlite3.connect(DB_PATH)

print("Writing to SQLite...")

df.to_sql(
    "historical_matches",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print(f"Loaded {len(df)} matches into historical_matches.")
