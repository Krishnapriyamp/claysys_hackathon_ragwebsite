def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list:
    print(f"DEBUG: Chunking text of length {len(text)} chars (approx {len(text.split())} words)")
    words = text.split()
    chunks = []
    
    if not words:
        return chunks
        
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        if i + chunk_size >= len(words):
            break
        i += chunk_size - overlap
        
    print(f"DEBUG: Created {len(chunks)} chunks")
    return chunks
