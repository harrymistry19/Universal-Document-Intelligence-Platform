import sqlite3
from app.config import DB_PATH, TABLE_NAME
from app.logger import logger


def initialize_db(cursor):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chunk_id INTEGER,
            section TEXT,
            content TEXT,
            content_hash TEXT UNIQUE,
            source_type TEXT
        )
    """)



def save(df):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    initialize_db(cursor)

    for _, row in df.iterrows():
        try:
            cursor.execute(
                f"""
                INSERT INTO {TABLE_NAME}
                (section, content, content_hash, source_type)
                VALUES (?, ?, ?, ?)
                """,
                (
                    row["section"],
                    row["content"],
                    row["content_hash"],
                    row["source_type"]
                )
            )
        except sqlite3.IntegrityError:
            logger.info("Duplicate skipped")

    conn.commit()
    conn.close()
