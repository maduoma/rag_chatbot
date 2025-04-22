import warnings
warnings.filterwarnings("ignore", message="CropBox missing from /Page, defaulting to MediaBox")

import os
import pdfplumber
import pandas as pd
from docx import Document

def load_document(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".txt":
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or '' for page in pdf.pages)
    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".csv":
        df = pd.read_csv(file_path)
        return df.to_string(index=False)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
