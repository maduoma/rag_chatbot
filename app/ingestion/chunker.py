def chunk_text(text: str, max_length: int = 2000) -> list:
    # Simple paragraph split, fallback to lines if too long
    paras = [p.strip() for p in text.split('\n') if p.strip()]
    chunks = []
    chunk = ""
    for para in paras:
        if len(chunk) + len(para) < max_length:
            chunk += ("\n" if chunk else "") + para
        else:
            if chunk:
                chunks.append(chunk)
            chunk = para
    if chunk:
        chunks.append(chunk)
    return chunks
