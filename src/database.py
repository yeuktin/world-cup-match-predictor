from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "worldcup.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


def get_connection():
    """Create a SQLite database connection."""
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """Create database tables from schema.sql."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        schema = SCHEMA_PATH.read_text()
        conn.executescript(schema)
        conn.commit()


def load_csvs_to_database():
    """Load mock CSV files into the SQLite database."""
    with get_connection() as conn:
        pd.read_csv(RAW_DATA_DIR / "teams.csv").to_sql("teams", conn, if_exists="append", index=False)
        pd.read_csv(RAW_DATA_DIR / "players.csv").to_sql("players", conn, if_exists="append", index=False)
        pd.read_csv(RAW_DATA_DIR / "matches.csv").to_sql("matches", conn, if_exists="append", index=False)
        conn.commit()


def run_query(query: str, params: tuple = ()): 
    """Run a SQL query and return a pandas DataFrame."""
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)


def save_prediction(team_a, team_b, probs, xg_a, xg_b):
    """Save prediction result to database for SQL portfolio proof."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO predictions
            (team_a, team_b, team_a_win_prob, draw_prob, team_b_win_prob, expected_goals_a, expected_goals_b)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (team_a, team_b, probs["team_a_win"], probs["draw"], probs["team_b_win"], xg_a, xg_b),
        )
        conn.commit()


if __name__ == "__main__":
    initialize_database()
    load_csvs_to_database()
    print(f"Database created at: {DB_PATH}")
