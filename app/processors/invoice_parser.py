import re


def extract_invoice_fields(df):
    """
    Best-effort invoice extraction WITHOUT ML.
    Uses line-based parsing + heuristics.
    """

    raw_text = "\n".join(df.astype(str).values.flatten())
    lines = [l.strip() for l in raw_text.split("\n") if len(l.strip()) > 3]

    invoice_number = "Not Found"
    total_amount = "Not Found"

    # -------------------------
    # Invoice Number (line-based)
    # -------------------------
    for line in lines:
        if re.search(r"invoice\s*(no|number)", line, re.IGNORECASE):
            match = re.search(r"([A-Z0-9\-\/]{4,})", line)
            if match:
                invoice_number = match.group(1)
                break

    # -------------------------
    # Total Amount (heuristic)
    # -------------------------
    amounts = []

    for line in lines:
        if re.search(r"total|grand\s*total|amount\s*due", line, re.IGNORECASE):
            nums = re.findall(r"\d{1,3}(?:,\d{3})*(?:\.\d{2})?", line)
            for n in nums:
                try:
                    amounts.append(float(n.replace(",", "")))
                except:
                    pass

    # Fallback: use largest numeric value in document
    if not amounts:
        nums = re.findall(r"\d{1,3}(?:,\d{3})*(?:\.\d{2})?", raw_text)
        for n in nums:
            try:
                amounts.append(float(n.replace(",", "")))
            except:
                pass

    if amounts:
        total_amount = f"{max(amounts):.2f}"

    return {
        "Invoice Number": invoice_number,
        "Total Amount": total_amount
    }
