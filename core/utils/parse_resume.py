import os
import pdfplumber
import docx

def extract_text_from_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        # Extract text from a searchable PDF
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    elif ext == ".docx":
        # Extract text from a DOCX file
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    else:
        raise ValueError("Unsupported file type: only PDF and DOCX are allowed.")

    return text.strip()
