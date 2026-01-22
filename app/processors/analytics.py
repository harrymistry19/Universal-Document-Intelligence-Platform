from collections import Counter
import re
from app.config import WORDS_PER_MINUTE


def document_analytics(df):
    text = " ".join(df.astype(str).values.flatten())
    words = re.findall(r"\b\w+\b", text.lower())

    return {
        "total_characters": len(text),
        "total_words": len(words),
        "total_chunks": len(df),
        "reading_time_minutes": round(len(words) / WORDS_PER_MINUTE, 2),
        "top_keywords": Counter(words).most_common(10)
    }
