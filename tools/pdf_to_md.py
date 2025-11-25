import pdfplumber

def pdf_to_markdown_tool(pdf_path: str) -> str:
    """Very simple PDF -> text/markdown extraction."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for p in pdf.pages:
            text = p.extract_text() or ""
            pages.append(text.strip())
    md = "\n\n".join(pages)
    return md
