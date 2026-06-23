# World Cup Match Predictor

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![SQL](https://img.shields.io/badge/SQL-SQLite-green?logo=sqlite)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange?logo=scikitlearn)
![Kaggle](https://img.shields.io/badge/Data-Kaggle-20BEFF?logo=kaggle)
![GitHub](https://img.shields.io/badge/Version_Control-GitHub-black?logo=github)

## Application Preview

### Home Screen

![Home Screen](screenshots/home.png)

### Match Prediction

![Match Prediction](screenshots/prediction.png)

### Team Analysis

![Team Analysis](screenshots/analysis.png)

---

## Overview

A sports analytics application that predicts international football match outcomes using machine learning, SQL, and historical match data.
A sports analytics application that predicts international football match outcomes using machine learning, SQL, and historical match data.

This project integrates **49,477 international football matches** dating back to **1872** from the Kaggle International Football Results dataset and uses SQL-powered analytics to generate:

- Match outcome probabilities
- Expected goals (xG)
- Team comparisons
- Historical performance metrics
- Scoreline forecasts

---

## Features

- Predict Team A win probability
- Predict draw probability
- Predict Team B win probability
- Estimate expected goals (xG)
- Generate likely scorelines
- Compare national teams side-by-side
- Display historical team statistics
- Store predictions in SQLite
- Interactive Streamlit dashboard

---

## Dataset

**Source:** Kaggle International Football Results Dataset

### Dataset Statistics

| Metric | Value |
|----------|----------|
| Historical Matches | 49,477 |
| Date Range | 1872 - Present |
| Data Source | Kaggle |
| Competition Types | International Matches |

The historical dataset is loaded into SQLite and used to generate team performance metrics and prediction features.

---

## Tech Stack

### Languages

- Python
- SQL

### Libraries

- pandas
- NumPy
- scikit-learn
- Streamlit

### Database

- SQLite

### Version Control

- Git
- GitHub

---

## Technical Skills Demonstrated

### Data Engineering

- CSV ingestion pipelines
- Data transformation
- SQLite database design
- Historical data integration

### SQL

- Relational database design
- Analytical queries
- Historical performance calculations
- Prediction storage and retrieval

### Machine Learning

- Match outcome prediction
- Expected goals estimation
- Feature engineering
- Model serialization with Joblib

### Software Development

- Modular Python architecture
- Interactive dashboard development
- Git version control

---

## Project Structure

```text
world-cup-match-predictor/
│
├── app/
├── src/
├── data/
├── database/
├── models/
│
├── setup_database.py
├── upgrade_world_cup_data.py
├── load_historical_matches.py
├── run_training.py
├── requirements.txt
└── README.md
```

---
## Running Locally

Follow these steps to run the project on your own computer.

### 1. Clone the repository

```bash
git clone https://github.com/yeuktin/world-cup-match-predictor.git
cd world-cup-match-predictor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If that does not work, try:

```bash
python3 -m pip install -r requirements.txt
```

### 3. Initialize the SQLite database

```bash
python3 setup_database.py
```

This creates the local SQLite database used by the app.

### 4. Load World Cup team data

```bash
python3 upgrade_world_cup_data.py
```

This loads the national team data required for predictions.

### 5. Launch the app

```bash
streamlit run app/app.py
```

The app should open in your browser at:

```text
http://localhost:8501
```

---

## Optional: Load Full Historical Kaggle Data

The app can also use the Kaggle International Football Results dataset for full historical analytics.

The full Kaggle dataset is not included in this repository.

To enable historical win rates, goals scored per match, goals allowed per match, and historical performance metrics:

### 1. Download the Kaggle dataset

Download the International Football Results dataset from Kaggle.

### 2. Create the external data folder

```bash
mkdir -p data/external
```

### 3. Add the Kaggle file

Place this file:

```text
results.csv
```

inside:

```text
data/external/
```

The file path should look like this:

```text
data/external/results.csv
```

### 4. Load historical matches into SQLite

```bash
python3 load_historical_matches.py
```

### 5. Confirm the data loaded

```bash
sqlite3 database/worldcup.db "SELECT COUNT(*) FROM historical_matches;"
```

Expected result:

```text
49477
```

or another number close to 49,000 depending on the Kaggle dataset version.

### 6. Run the app again

```bash
streamlit run app/app.py
```

---

## Quick Start Commands

For the basic version of the app:

```bash
git clone https://github.com/yeuktin/world-cup-match-predictor.git
cd world-cup-match-predictor
pip install -r requirements.txt
python3 setup_database.py
python3 upgrade_world_cup_data.py
streamlit run app/app.py
```

For the full version with historical Kaggle analytics, download `results.csv`, place it in `data/external/`, then run:

```bash
python3 load_historical_matches.py
streamlit run app/app.py
```
---

## Resume Description

Built a World Cup Match Predictor using Python, SQL, SQLite, Streamlit, and machine learning. Integrated 49,477 historical international football matches from Kaggle, designed a relational database, engineered predictive features, trained machine learning models, and developed an interactive analytics dashboard for match forecasting and team comparison.
