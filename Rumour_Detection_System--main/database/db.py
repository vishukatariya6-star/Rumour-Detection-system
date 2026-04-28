import sqlite3
import os

DB_PATH = "data/news.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            headline TEXT,
            result TEXT,
            confidence REAL
        )
    """)

    conn.commit()
    conn.close()

def save_result(headline, result, confidence):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO history (headline, result, confidence) VALUES (?, ?, ?)",
        (headline, result, confidence)
    )

    conn.commit()
    conn.close()

def load_history(limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT headline, result, confidence
        FROM history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = c.fetchall()
    conn.close()
    return rows