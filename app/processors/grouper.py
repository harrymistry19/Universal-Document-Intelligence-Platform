def group_chunks(df):
    groups = []

    if "section" not in df.columns:
        return groups

    for section in df["section"].unique():
        chunks = df[df["section"] == section]["content"].tolist()
        groups.append({
            "group_title": section,
            "chunks": chunks
        })

    return groups
