DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS predictions;

CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT UNIQUE NOT NULL,
    confederation TEXT,
    fifa_rank INTEGER,
    attack_rating REAL,
    defense_rating REAL,
    midfield_rating REAL,
    form_rating REAL
);

CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT NOT NULL,
    team_name TEXT NOT NULL,
    position TEXT,
    goals_per_90 REAL,
    starter_rating REAL,
    FOREIGN KEY(team_name) REFERENCES teams(team_name)
);

CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY,
    date TEXT,
    team_a TEXT NOT NULL,
    team_b TEXT NOT NULL,
    team_a_goals INTEGER,
    team_b_goals INTEGER,
    tournament TEXT,
    FOREIGN KEY(team_a) REFERENCES teams(team_name),
    FOREIGN KEY(team_b) REFERENCES teams(team_name)
);

CREATE TABLE predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    team_a TEXT,
    team_b TEXT,
    team_a_win_prob REAL,
    draw_prob REAL,
    team_b_win_prob REAL,
    expected_goals_a REAL,
    expected_goals_b REAL
);
