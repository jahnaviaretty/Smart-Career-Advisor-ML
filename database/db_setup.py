
import sqlite3
from pathlib import Path

# Locate database folder
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "career_advisor.db"

# Connect to SQLite database
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Create career prediction history table
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    career TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

connection.commit()
connection.close()

print("Database created successfully!")
print("Database location:", DB_PATH)

