import sqlite3
from datetime import datetime
from app.config import DB_PATH

def log_run(source, input_value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            input_value TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO runs (source, input_value, timestamp) VALUES (?, ?, ?)",
        (source, input_value, datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()
