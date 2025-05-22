# utils/pdf_reader.py

import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    texts = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            texts.append({
                "page": i + 1,
                "text": text
            })
    return texts
