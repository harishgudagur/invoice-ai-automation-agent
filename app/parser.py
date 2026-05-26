import fitz
import pytesseract
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

tesseract_path = os.getenv("TESSERACT_PATH")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text_from_pdf(file_path):
    """
    Extract text from PDF using PyMuPDF.
    """
    try:
        text = ""

        pdf = fitz.open(file_path)

        for page in pdf:
            text += page.get_text()

        pdf.close()

        if not text.strip():
            raise ValueError("No readable text found in PDF")

        return text.strip()

    except Exception as e:
        raise Exception(f"PDF Parsing Failed: {str(e)}")


def extract_text_from_image(file_path):
    """
    OCR extraction for scanned invoices.
    """
    try:
        image = Image.open(file_path)

        text = pytesseract.image_to_string(image)

        if not text.strip():
            raise ValueError("OCR returned empty text")

        return text.strip()

    except Exception as e:
        raise Exception(f"OCR Failed: {str(e)}")


def parse_document(file_path):
    """
    Decide parser based on extension.
    """
    extension = file_path.split(".")[-1].lower()

    if extension == "pdf":
        return extract_text_from_pdf(file_path)

    elif extension in ["jpg", "jpeg", "png"]:
        return extract_text_from_image(file_path)

    else:
        raise Exception("Unsupported file type")