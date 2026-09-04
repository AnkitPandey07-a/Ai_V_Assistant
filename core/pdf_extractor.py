import fitz


def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from all pages of a PDF."""

    document = fitz.open(pdf_path)

    text: list[str] = []

    for page in document:
        page_text = page.get_text("text")

        if isinstance(page_text, str) and page_text.strip():
            text.append(page_text)

    document.close()

    return "\n".join(text).strip()