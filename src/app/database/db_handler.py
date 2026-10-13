import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'agro_ai.db')

def init_db():
    """Initializes SQLite Database tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Master Crops Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master_crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            soil TEXT NOT NULL,
            season TEXT NOT NULL,
            best_time TEXT NOT NULL,
            technique TEXT NOT NULL,
            tools TEXT NOT NULL,
            crop_rotation TEXT NOT NULL
        )
    ''')

    # User Crops Table (Push / Pop target)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_name TEXT NOT NULL
        )
    ''')

    # Expense & Ledger Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            entry_type TEXT NOT NULL,
            entry_date TEXT NOT NULL
        )
    ''')

    # Seed sample master crops if empty
    cursor.execute('SELECT COUNT(*) FROM master_crops')
    if cursor.fetchone()[0] == 0:
        sample_crops = [
            ("Wheat", "Loamy / Clay", "Rabi (Winter)", "Oct - Nov", "Line sowing with drill", "Tractor, Seed Drill", "Rotate with Legumes"),
            ("Rice", "Clayey Loam", "Kharif (Monsoon)", "Jun - Jul", "Transplanting method", "Transplanter, Harvester", "Rotate with Pulses"),
            ("Tomato", "Well-Drained Sandy Loam", "Zaad / Summer", "Feb - Mar", "Raised bed with drip", "Drip Kit, Mulching Sheet", "Rotate with Corn"),
            ("Potato", "Loose Sandy Soil", "Rabi (Winter)", "Oct - Nov", "Tuber bed ridging", "Ridger, Digger", "Rotate with Mustard"),
            ("Cotton", "Black Soil (Regur)", "Kharif (Monsoon)", "May - Jun", "Dibbling at wide spacing", "Cotton Picker, Sprayer", "Rotate with Groundnut")
        ]
        cursor.executemany('''
            INSERT INTO master_crops (name, soil, season, best_time, technique, tools, crop_rotation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_crops)

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
