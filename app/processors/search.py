def search_chunks(df, query):
    mask = df["content"].str.contains(query, case=False, na=False)
    return df[mask]
