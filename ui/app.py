import sys
import os
import sqlite3

# -------------------------------------------------
# Ensure project root is in Python path (CRITICAL)
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# -------------------------------------------------
# Imports AFTER path fix
# -------------------------------------------------
import streamlit as st
import pandas as pd

from app.core.orchestrator import run
from app.processors.grouper import group_chunks
from app.processors.search import search_chunks
from app.processors.semantic_search import semantic_search
from app.processors.analytics import document_analytics
from app.processors.invoice_parser import extract_invoice_fields
from app.processors.summarizer import summarize_document
from app.storage.history import save_document


# -------------------------------------------------
# Session State Initialization
# -------------------------------------------------
if "df" not in st.session_state:
    st.session_state.df = None


# -------------------------------------------------
# Helper Functions
# -------------------------------------------------
def get_full_text_from_df(df):
    text_columns = ["content", "text", "value"]
    collected = []

    for col in text_columns:
        if col in df.columns:
            collected.extend(df[col].astype(str).tolist())

    if not collected:
        collected = df.astype(str).agg(" ".join, axis=1).tolist()

    return "\n\n".join(collected)


# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Universal Web Scraper",
    page_icon="🌐",
    layout="wide"
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("🌐 Universal Web Scraping Platform")
st.subheader(
    "Scrape Websites, PDFs & Images — Structured, Searchable & Intelligent"
)
st.markdown("---")

# -------------------------------------------------
# Input Section
# -------------------------------------------------
input_type = st.radio(
    "Select Input Type",
    ["Website URL", "PDF File", "Image File"],
    horizontal=True
)

input_value = None

if input_type == "Website URL":
    input_value = st.text_input("Enter website URL")

elif input_type == "PDF File":
    uploaded = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded:
        os.makedirs("data/raw", exist_ok=True)
        path = f"data/raw/{uploaded.name}"
        with open(path, "wb") as f:
            f.write(uploaded.read())
        input_value = path

elif input_type == "Image File":
    uploaded = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if uploaded:
        os.makedirs("data/raw", exist_ok=True)
        path = f"data/raw/{uploaded.name}"
        with open(path, "wb") as f:
            f.write(uploaded.read())
        input_value = path

# -------------------------------------------------
# Action Button
# -------------------------------------------------
if st.button("🚀 Extract Data", use_container_width=True):

    if not input_value:
        st.warning("Please provide a valid input.")
    else:
        with st.spinner("Extracting and processing data..."):
            st.session_state.df = run(input_value)
            save_document(input_value, st.session_state.df)

        st.success("Data extracted and saved successfully!")
        st.markdown("---")

# -------------------------------------------------
# MAIN CONTENT
# -------------------------------------------------
if st.session_state.df is not None:

    df = st.session_state.df

    # -----------------------------
    # Extracted Content
    # -----------------------------
    st.markdown("## 📄 Extracted Content")

    if "section" in df.columns and "content" in df.columns:
        for section in df["section"].unique():
            st.markdown(f"### {section}")
            for text in df[df["section"] == section]["content"]:
                st.write(text)
    else:
        st.write("No structured sections found.")

    st.markdown("---")

    # -----------------------------
    # Grouped Semantic Content
    # -----------------------------
    if "chunk_id" in df.columns and "section" in df.columns:
        st.markdown("## 🧠 Grouped Semantic Content")

        grouped = group_chunks(df)
        for i, group in enumerate(grouped, start=1):
            with st.expander(f"📌 Group {i}: {group['group_title']}"):
                for chunk in group["chunks"]:
                    st.write(chunk)

    st.markdown("---")

    # -----------------------------
    # Keyword Search
    # -----------------------------
    st.markdown("## 🔍 Keyword Search")

    search_query = st.text_input("Search exact words")

    if search_query:
        results = search_chunks(df, search_query)
        if results.empty:
            st.info("No keyword matches found.")
        else:
            for _, row in results.iterrows():
                with st.expander(row.get("section", "Content")):
                    st.markdown(row["content"])

    st.markdown("---")

    # -----------------------------
    # Semantic Search
    # -----------------------------
    st.markdown("## 🧠 Semantic Search (AI-Ready)")

    semantic_query = st.text_input("Search by meaning")

    if semantic_query and "content" in df.columns:
        semantic_results = semantic_search(df, semantic_query)

        if semantic_results.empty:
            st.info("No semantic matches found.")
        else:
            for _, row in semantic_results.iterrows():
                with st.expander(row.get("section", "Content")):
                    st.write(row["content"])

    st.markdown("---")

    # -----------------------------
    # Document Analytics
    # -----------------------------
    st.markdown("## 📊 Document Analytics")

    stats = document_analytics(df)
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Characters", stats["total_characters"])
    c2.metric("Words", stats["total_words"])
    c3.metric("Chunks", stats["total_chunks"])
    c4.metric("Reading Time (min)", stats["reading_time_minutes"])

    st.dataframe(
        pd.DataFrame(stats["top_keywords"], columns=["Keyword", "Frequency"]),
        use_container_width=True
    )

    st.markdown("---")

    # -----------------------------
    # Document History
    # -----------------------------
    st.markdown("## 🗂 Document History")

    conn = sqlite3.connect("data/history.db")
    history_df = pd.read_sql(
        "SELECT * FROM documents ORDER BY created_at DESC", conn
    )
    conn.close()

    st.dataframe(history_df, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Document Comparison
    # -----------------------------
    st.markdown("## 🔁 Document Comparison")

    if len(history_df) >= 2:
        d1 = st.selectbox("Document 1", history_df["id"])
        d2 = st.selectbox("Document 2", history_df["id"], index=1)

        if st.button("Compare"):
            from app.processors.comparator import compare_documents

            t1 = history_df[history_df["id"] == d1]["content"].values[0]
            t2 = history_df[history_df["id"] == d2]["content"].values[0]

            st.metric("Similarity %", compare_documents(t1, t2))

    st.markdown("---")

    # -----------------------------
    # Invoice Intelligence
    # -----------------------------
    st.markdown("## 🧾 Invoice Intelligence (Heuristic)")

    invoice_df = pd.DataFrame(
        extract_invoice_fields(df).items(),
        columns=["Field", "Value"]
    )
    st.dataframe(invoice_df, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # AI Summary
    # -----------------------------
    st.markdown("## 🤖 AI-Like Summary")

    for i, line in enumerate(summarize_document(df), start=1):
        st.markdown(f"**{i}.** {line}")

    st.markdown("---")

    # -----------------------------
    # Download
    # -----------------------------
    st.markdown("## ⬇️ Download")

    st.download_button(
        "Download TXT",
        get_full_text_from_df(df),
        "extracted.txt",
        "text/plain"
    )

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "extracted.csv",
        "text/csv"
    )

else:
    st.info("Please extract data to enable features.")
