import pdfplumber
import pytesseract
from PIL import Image



def extract(pdf_path):
    paragraphs = []
    full_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    if len(line.strip()) > 40:
                        paragraphs.append(line.strip())
                        full_text.append(line.strip())

    # OCR fallback if no text
    if not full_text:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                image = page.to_image(resolution=300).original
                text = pytesseract.image_to_string(image)
                for line in text.split("\n"):
                    if len(line.strip()) > 40:
                        paragraphs.append(line.strip())
                        full_text.append(line.strip())

    return [{
        "title": "PDF Document",
        "headings": [],
        "paragraphs": paragraphs
    }]
