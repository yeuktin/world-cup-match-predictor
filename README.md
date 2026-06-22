# World Cup Match Predictor 

A public portfolio project that predicts international football match outcomes using **Python, SQL, machine learning, SQLite, pandas, scikit-learn, Plotly, and Streamlit**.

This project is designed as an  first: it uses mock CSV data so the app works immediately, while keeping the structure ready for real World Cup data from Kaggle, StatsBomb open data, or a football API.

## Features

- Select two national teams
- Predict Team A win probability, draw probability, and Team B win probability
- Estimate expected goals for both teams
- Show most likely scorelines with probabilities
- Show likely goal scorers and player scoring probabilities
- Store predictions in a SQLite database
- Display SQL-powered views inside the app
- Deployable with Streamlit Community Cloud

## Skills Demonstrated

- **Python:** pandas, numpy, modular project structure
- **SQL:** SQLite schema, relational tables, SQL queries, prediction storage
- **Machine Learning:** scikit-learn classification and regression models
- **Data Engineering:** CSV ingestion into SQL database
- **Data Visualization:** Plotly charts in Streamlit
- **Deployment:** Streamlit app ready for public portfolio use
- **GitHub:** clean repo structure and documentation

## Project Structure

```text
world_cup_predictor_mvp/
  app/
    app.py
  data/
    raw/
      teams.csv
      players.csv
      matches.csv
  database/
    schema.sql
  models/
  src/
    database.py
    features.py
    predict.py
    train_model.py
  setup_database.py
  run_training.py
  requirements.txt
  README.md
  .gitignore
```

## Local Setup

### 1. Open the folder in VS Code

```bash
cd world_cup_predictor_mvp
code .
```

### 2. Create a virtual environment

Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the SQLite database

```bash
python setup_database.py
```

### 5. Train the machine learning models

```bash
python run_training.py
```

### 6. Run the Streamlit app

```bash
streamlit run app/app.py
```

## How the App Works

```text
Mock CSV Data
↓
SQLite Database
↓
SQL Queries
↓
Python Feature Engineering
↓
Machine Learning Models
↓
Streamlit Dashboard
↓
Saved Predictions Back Into SQL
```

## Database Tables

### teams
Stores team-level ratings and FIFA ranking.

### players
Stores player-level scoring metrics.

### matches
Stores historical match results used for training.

### predictions
Stores app-generated predictions, proving SQL write-back functionality.

## Important  Note

The current dataset is mock/sample data. It is not meant for real betting or accurate forecasting. The goal of this  is to prove the full technical workflow and create a strong public portfolio project.

## Future Features

- Replace mock data with real World Cup data
- Add API ingestion pipeline
- Add Elo ratings
- Add team form over last 5 matches
- Add Monte Carlo tournament simulation
- Add player injury/news inputs
- Add match venue and home advantage
- Add model evaluation dashboard
- Add Docker support
- Add automated tests

## Resume Bullet Example

Built and deployed a World Cup match prediction web application using Python, SQL, SQLite, scikit-learn, pandas, Plotly, and Streamlit. Designed a relational database, engineered team and player features, trained machine learning models, and created an interactive dashboard for match outcome probabilities, scoreline forecasts, expected goals, and player scoring probabilities.
