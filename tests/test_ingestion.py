import pytest
# from app.ingestion import process_pdf, process_docx, process_csv
from app.ingestion import load_document, chunk_text
def test_load_document_exists():
    # This is a placeholder test to check load_document is callable
    assert callable(load_document)

# Example chunk_text test

def test_chunk_text():
    chunks = chunk_text("This is a test.\nAnother paragraph.")
    assert isinstance(chunks, list)
    assert all(isinstance(c, str) for c in chunks)
