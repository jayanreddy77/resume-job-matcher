import fitz


def extract_resume_text(pdf_file):
    """
    Extract text from a PDF resume.

    Args:
        pdf_file: Uploaded PDF file.

    Returns:
        Extracted text as a string.
    """

    extracted_text = []

    with fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    ) as document:

        for page in document:
            text = page.get_text()
            extracted_text.append(text)

    return "\n".join(extracted_text)