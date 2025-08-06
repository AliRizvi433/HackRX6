import os
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_file(file_path: str) -> str:
    """
    Extracts text from PDF, DOCX, TXT, or EML files based on file extension.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        try:
            reader = PdfReader(file_path)
            return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {e}")

    elif ext == ".docx":
        try:
            doc = Document(file_path)
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)
        except Exception as e:
            raise ValueError(f"Failed to extract text from DOCX: {e}")

    elif ext in [".txt", ".eml"]:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Failed to read text file: {e}")

    else:
        raise ValueError(f"Unsupported file type: {ext}")
