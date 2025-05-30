import fitz  # PyMuPDF
from loguru import logger

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    texts = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            texts.append({"page": i + 1, "text": text})
    logger.info(f"Extracted {len(texts)} pages from PDF.")
    return texts
