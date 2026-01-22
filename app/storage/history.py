import sqlite3
from datetime import datetime
from app.config import HISTORY_DB_PATH


def save_document(source, df):
    conn = sqlite3.connect(HISTORY_DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            content TEXT,
            created_at TEXT
        )
    """)

    text = "\n".join(df.astype(str).values.flatten())

    cur.execute(
        "INSERT INTO documents (source, content, created_at) VALUES (?, ?, ?)",
        (source, text, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()
