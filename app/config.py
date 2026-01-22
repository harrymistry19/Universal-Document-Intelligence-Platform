# app/config.py

BASE_URL = "https://quotes.toscrape.com"

REQUEST_TIMEOUT = 10
MAX_RETRIES = 3

# -----------------------------
# Paths
# -----------------------------
RAW_DATA_DIR = "data/raw"
HISTORY_DB_PATH = "data/history.db"
LOG_DIR = "logs"

# -----------------------------
# Semantic Search
# -----------------------------
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
SEMANTIC_TOP_K = 5

# -----------------------------
# Analytics
# -----------------------------
WORDS_PER_MINUTE = 200

DATA_DIR = "data"
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
ARCHIVE_DIR = "data/archive"

DB_PATH = "database/ingestion.db"

LOG_FILE = "logs/pipeline.log"

TABLE_NAME = "ingested_data"
