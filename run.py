import sys
from app.core.pipeline import run_pipeline

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run.py <url | pdf | image>")
        sys.exit(1)

    run_pipeline(sys.argv[1])
