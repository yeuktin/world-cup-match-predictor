import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("database/worldcup.db")

WORLD_CUP_TEAMS = [
    ("Mexico","CONCACAF","A",15,78,76,77,7),
    ("South Africa","CAF","A",61,68,67,68,5),
    ("South Korea","AFC","A",22,77,74,76,7),
    ("Czechia","UEFA","A",44,72,73,73,5),
    ("Canada","CONCACAF","B",31,76,72,74,7),
    ("Bosnia and Herzegovina","UEFA","B",70,68,67,68,5),
    ("Qatar","AFC","B",58,68,66,67,4),
    ("Switzerland","UEFA","B",19,78,78,78,7),
    ("Brazil","CONMEBOL","C",5,88,82,85,8),
    ("Morocco","CAF","C",12,80,79,80,7),
    ("Haiti","CONCACAF","C",90,63,62,63,4),
    ("Scotland","UEFA","C",39,73,74,74,6),
    ("United States","CONCACAF","D",13,80,76,78,8),
    ("Paraguay","CONMEBOL","D",55,70,71,70,5),
    ("Australia","AFC","D",24,75,73,74,6),
    ("Turkey","UEFA","D",28,77,74,76,6),
    ("Germany","UEFA","E",9,85,82,84,8),
    ("Curacao","CONCACAF","E",85,64,62,63,4),
    ("Ivory Coast","CAF","E",42,74,72,73,6),
    ("Ecuador","CONMEBOL","E",30,75,74,75,6),
    ("Netherlands","UEFA","F",7,84,82,83,8),
    ("Japan","AFC","F",18,79,76,78,7),
    ("Sweden","UEFA","F",25,76,75,76,6),
    ("Tunisia","CAF","F",49,70,70,70,5),
    ("Belgium","UEFA","G",8,84,79,82,7),
    ("Egypt","CAF","G",34,76,72,74,6),
    ("Iran","AFC","G",20,76,73,75,6),
    ("New Zealand","OFC","G",88,64,63,64,4),
    ("Spain","UEFA","H",3,87,84,86,8),
    ("Cape Verde","CAF","H",65,67,66,67,5),
    ("Saudi Arabia","AFC","H",56,69,68,69,5),
    ("Uruguay","CONMEBOL","H",11,82,80,81,7),
    ("France","UEFA","I",2,89,84,87,8),
    ("Senegal","CAF","I",17,79,77,78,7),
    ("Iraq","AFC","I",59,69,67,68,5),
    ("Norway","UEFA","I",43,79,72,75,6),
    ("Argentina","CONMEBOL","J",1,89,83,86,8),
    ("Algeria","CAF","J",37,75,72,74,6),
    ("Austria","UEFA","J",23,78,76,77,6),
    ("Jordan","AFC","J",71,66,65,66,4),
    ("Portugal","UEFA","K",6,86,81,84,8),
    ("DR Congo","CAF","K",64,68,67,68,5),
    ("Uzbekistan","AFC","K",57,69,68,69,5),
    ("Colombia","CONMEBOL","K",14,81,78,80,7),
    ("England","UEFA","L",4,87,83,85,8),
    ("Croatia","UEFA","L",10,81,80,81,7),
    ("Ghana","CAF","L",47,72,70,71,5),
    ("Panama","CONCACAF","L",45,70,69,70,5),
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DELETE FROM teams")

for i, team in enumerate(WORLD_CUP_TEAMS, start=1):
    name, confed, group, rank, attack, defense, midfield, form = team
    cur.execute("""
        INSERT INTO teams
        (team_id, team_name, confederation, fifa_rank, attack_rating, defense_rating, midfield_rating, form_rating, world_cup_group)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (i, name, confed, rank, attack, defense, midfield, form, group))

cur.execute("""
CREATE TABLE IF NOT EXISTS historical_matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_date TEXT,
    home_team TEXT,
    away_team TEXT,
    home_score INTEGER,
    away_score INTEGER,
    tournament TEXT,
    city TEXT,
    country TEXT,
    neutral INTEGER,
    result TEXT,
    total_goals INTEGER
)
""")

conn.commit()
conn.close()

pd.DataFrame(WORLD_CUP_TEAMS, columns=[
    "team_name","confederation","world_cup_group","fifa_rank",
    "attack_rating","defense_rating","midfield_rating","form_rating"
]).to_csv("data/world_cup_2026_teams.csv", index=False)

print("Upgrade complete: 48 World Cup teams added.")
