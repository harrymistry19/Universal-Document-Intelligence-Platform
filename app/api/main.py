from fastapi import FastAPI, UploadFile, File
from app.core.pipeline import run_pipeline

app = FastAPI(title="Universal Data Ingestion API")

@app.post("/ingest/url")
def ingest_url(url: str):
    run_pipeline(url)
    return {"status": "success", "input": url}

@app.post("/ingest/file")
async def ingest_file(file: UploadFile = File(...)):
    path = f"data/raw/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    run_pipeline(path)
    return {"status": "success", "file": file.filename}
