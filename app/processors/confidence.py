def confidence_score(df):
    if "content" not in df.columns:
        return 0.0

    avg_length = df["content"].astype(str).apply(len).mean()

    if avg_length > 500:
        return 0.9
    elif avg_length > 200:
        return 0.7
    elif avg_length > 50:
        return 0.5
    else:
        return 0.3
