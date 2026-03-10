import sqlite3
import json
from config import DB_FILE

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            crude_barrels REAL,
            oil_price REAL,
            refining_fee REAL,
            total_value REAL,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_calculation(crude_barrels, oil_price, refining_fee, total_value, details):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO calculations (crude_barrels, oil_price, refining_fee, total_value, details)
        VALUES (?, ?, ?, ?, ?)
    ''', (crude_barrels, oil_price, refining_fee, total_value, json.dumps(details)))
    conn.commit()
    conn.close()

def get_history(limit=50):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(f"SELECT * FROM calculations ORDER BY timestamp DESC LIMIT {limit}", conn)
    conn.close()
    return df
