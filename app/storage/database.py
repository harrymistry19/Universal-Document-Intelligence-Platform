import sqlite3
import os

DB_PATH = "data/ingestion.db"


def save(df):
    """
    Save extracted structured data into SQLite.
    Cloud-safe, schema-flexible.
    """
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    # Let pandas handle schema automatically
    df.to_sql(
        "ingested_data",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()
