from src.database import initialize_database, load_csvs_to_database

if __name__ == "__main__":
    initialize_database()
    load_csvs_to_database()
    print("SQLite database initialized successfully.")
