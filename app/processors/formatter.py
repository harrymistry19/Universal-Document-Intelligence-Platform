import pandas as pd
from app.processors.hasher import generate_hash
from app.processors.chunker import semantic_chunk


def format_data(data, source_type):
    records = []
    item = data[0]

    sections = []

    if "title" in item:
        sections.append(("Title", item["title"]))

    for h in item.get("headings", []):
        sections.append(("Heading", h))

    for p in item.get("paragraphs", []):
        sections.append(("Paragraph", p))

    chunk_id = 1

    for section, content in sections:
        chunks = semantic_chunk(content)

        for chunk in chunks:
            records.append({
                "chunk_id": chunk_id,
                "section": section,
                "content": chunk,
                "source_type": source_type,
                "content_hash": generate_hash(chunk)
            })
            chunk_id += 1

    return pd.DataFrame(records)
