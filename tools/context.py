def chunk_text(text: str, chunk_size: int = 3500, overlap: int = 300):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+chunk_size])
        i += chunk_size - overlap
    return chunks

def compact_context(text: str, max_chars: int = 12000):
    """Keep head, middle, tail so long papers fit in context."""
    if len(text) <= max_chars:
        return text
    head = text[: max_chars//3]
    mid_start = len(text)//2 - max_chars//6
    mid = text[mid_start: mid_start + max_chars//3]
    tail = text[-max_chars//3 :]
    return head + "\n...\n" + mid + "\n...\n" + tail
