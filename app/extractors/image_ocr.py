import pytesseract
from PIL import Image


def extract(image_path):
    """
    OCR extractor for images (invoices, documents, screenshots).
    Returns structured data compatible with the pipeline.
    """

    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    # Clean & split into meaningful lines
    lines = [
        line.strip()
        for line in text.split("\n")
        if len(line.strip()) > 5
    ]

    return [{
        "title": "Image Document",
        "headings": [],
        "paragraphs": lines
    }]
