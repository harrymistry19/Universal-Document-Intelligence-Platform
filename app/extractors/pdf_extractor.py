import pdfplumber
import pytesseract
import shutil


def extract(pdf_path):
    extracted_text = []

    # 1️⃣ TEXT-based extraction (fast & preferred)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    extracted_text.append(text)
    except Exception:
        pass

    if extracted_text:
        return extracted_text

    # 2️⃣ OCR fallback (HF supports this)
    if shutil.which("tesseract") is None:
        return [
            "OCR engine not available in this environment."
        ]

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            image = page.to_image(resolution=300).original
            text = pytesseract.image_to_string(image)
            if text.strip():
                extracted_text.append(text)

    return extracted_text
