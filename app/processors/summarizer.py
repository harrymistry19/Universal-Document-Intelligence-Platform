import re
from collections import Counter


def summarize_document(df, max_sentences=5):
    text_columns = ["content", "text", "value"]
    texts = []

    for col in text_columns:
        if col in df.columns:
            texts.extend(df[col].astype(str).tolist())

    # Clean + deduplicate
    texts = list(set(t.strip() for t in texts if len(t.strip()) > 50))

    if not texts:
        return ["No sufficient content available for summarization."]

    full_text = " ".join(texts)

    sentences = re.split(r'(?<=[.!?])\s+', full_text)

    words = re.findall(r'\b[a-zA-Z]{3,}\b', full_text.lower())
    freq = Counter(words)

    scored = []
    for sent in sentences:
        score = sum(freq.get(w.lower(), 0) for w in sent.split())
        scored.append((score, sent))

    scored.sort(reverse=True)
    return [s for _, s in scored[:max_sentences]]
