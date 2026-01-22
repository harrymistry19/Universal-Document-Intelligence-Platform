import pdfplumber
import pytesseract
from PIL import Image
import shutil


def extract(pdf_path):
    extracted_text = []

    # 1️⃣ Try TEXT extraction first (Cloud-safe)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    extracted_text.append(text)
    except Exception:
        pass

    # If text was found, RETURN it (NO OCR)
    if extracted_text:
        return extracted_text

    # 2️⃣ OCR fallback ONLY if Tesseract exists
    if shutil.which("tesseract") is None:
        # Cloud-safe graceful fallback
        return [
            "⚠ This PDF appears to be scanned. "
            "OCR is not available in this deployment environment."
        ]

    # 3️⃣ OCR extraction (local only)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                image = page.to_image(resolution=300).original
                text = pytesseract.image_to_string(image)
                if text.strip():
                    extracted_text.append(text)
    except Exception as e:
        extracted_text.append(f"OCR failed: {str(e)}")

    return extracted_text
