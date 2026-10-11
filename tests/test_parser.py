from io import BytesIO

import fitz

from src.resume_parser import extract_resume_text


def test_extract_resume_text():
    # Create a PDF in memory.
    pdf_document = fitz.open()

    page = pdf_document.new_page()

    page.insert_text((50, 50), "Python Java SQL")

    pdf_bytes = pdf_document.tobytes()

    pdf_document.close()

    # Convert PDF bytes into a file-like object.
    pdf_file = BytesIO(pdf_bytes)

    # Extract the text.
    result = extract_resume_text(pdf_file)

    # Verify the extracted text.
    assert "Python" in result
    assert "Java" in result
    assert "SQL" in result