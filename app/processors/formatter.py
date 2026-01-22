import pandas as pd


def format_data(data, source):
    """
    Normalize extracted data from different sources (URL, PDF, Image)
    into a single structured DataFrame.

    This function is cloud-safe and type-safe.
    """

    rows = []

    # Case 1: data is list (PDF pages, OCR text, etc.)
    if isinstance(data, list):
        for idx, item in enumerate(data):
            if isinstance(item, dict):
                content = item.get("content", "")
                section = item.get("section", f"Page {idx+1}")
            else:
                # item is string
                content = str(item)
                section = f"Page {idx+1}"

            if content.strip():
                rows.append({
                    "source_type": source,
                    "section": section,
                    "chunk_id": idx + 1,
                    "content": content.strip()
                })

    # Case 2: data is dict (HTML structured extraction)
    elif isinstance(data, dict):
        content = data.get("content", "")
        section = data.get("section", "Content")

        if content.strip():
            rows.append({
                "source_type": source,
                "section": section,
                "chunk_id": 1,
                "content": content.strip()
            })

    # Case 3: fallback (string or unknown)
    else:
        rows.append({
            "source_type": source,
            "section": "Content",
            "chunk_id": 1,
            "content": str(data)
        })

    return pd.DataFrame(rows)
