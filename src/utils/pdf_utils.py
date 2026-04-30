from typing import Optional
from pypdf import PdfReader


def extract_text_from_pdf(path: str) -> str:
    """Return extracted text from all pages of a PDF file.

    Args:
        path: Path to the PDF file.

    Returns:
        Combined text from all pages.
    """
    reader = PdfReader(path)
    text_parts = []
    for page in reader.pages:
        page_text: Optional[str] = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n".join(text_parts)
