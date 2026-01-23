# 🌐 Universal Document Intelligence Platform

A production-style web application that extracts, analyzes, and searches content
from **websites, PDFs, and images** using a structured data pipeline and AI-ready techniques.

This project demonstrates real-world data ingestion, processing, storage, analytics,
and semantic search — designed with scalability and industry practices in mind.

---

## 🛠 Tech Stack

streamlit
pandas
numpy
requests
beautifulsoup4
pytesseract
Pillow
pdfplumber
sentence-transformers
scikit-learn
torch


## 🚀 Features

- 🌍 Web scraping (static websites)
- 📄 PDF text extraction
- 🖼 Image OCR extraction
- 🧱 Structured semantic chunking
- 🔍 Keyword-based search
- 🧠 Semantic (embedding-based) search
- 📊 Document analytics dashboard
- 🤖 AI-like document summarization
- 🗂 SQLite-backed document history
- 🔁 Document comparison
- 📦 Batch-ready ingestion pipeline
- 📝 Logging for observability

---


---

## 🧠 Use Cases

- Research & article analysis
- Invoice and document review
- Knowledge extraction systems
- RAG / LLM-ready pipelines
- Data ingestion & preprocessing

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run ui/app.py



app/
 ├── core/
 ├── extractors/
 ├── processors/
 ├── storage/
 ├── config.py
 └── logger.py
ui/
 └── app.py
data/
 ├── raw/
 └── history.db




🔮 Future Enhancements

RAG with LLMs (OpenAI / local models)

Authentication & multi-user support

Dockerization

Cloud storage integration