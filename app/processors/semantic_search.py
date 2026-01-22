import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL_NAME, SEMANTIC_TOP_K


@st.cache_resource
def load_model():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def semantic_search(df, query, top_k=SEMANTIC_TOP_K):
    if "content" not in df.columns:
        return df.iloc[0:0]

    model = load_model()
    texts = df["content"].astype(str).tolist()

    text_embeddings = model.encode(texts, show_progress_bar=False)
    query_embedding = model.encode([query])[0]

    scores = np.dot(text_embeddings, query_embedding)
    top_indices = np.argsort(scores)[::-1][:top_k]

    return df.iloc[top_indices]
