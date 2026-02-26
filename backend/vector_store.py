import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize Model
MODEL_NAME = 'all-MiniLM-L6-v2'
print(f"DEBUG: Loading embedding model {MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME)

INDEX_FILE = 'faiss_index.bin'
CHUNKS_FILE = 'chunks.json'

def create_and_save_index(chunks: list) -> int:
    if not chunks:
        return 0
        
    print(f"DEBUG: Encoding {len(chunks)} chunks into embeddings...")
    embeddings = model.encode(chunks, convert_to_numpy=True)
    embeddings = np.array(embeddings).astype('float32')
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    faiss.write_index(index, INDEX_FILE)
    
    with open(CHUNKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
        
    print(f"DEBUG: Saved {INDEX_FILE} and {CHUNKS_FILE} locally.")
    print(f"DEBUG: Created {len(chunks)} chunks in total.")
    print(f"DEBUG: Created {embeddings.shape[0]} embeddings.")
    
    return len(chunks)

def load_index_and_chunks():
    if not os.path.exists(INDEX_FILE) or not os.path.exists(CHUNKS_FILE):
        return None, None
        
    index = faiss.read_index(INDEX_FILE)
    with open(CHUNKS_FILE, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
        
    return index, chunks

def clear_index():
    print("DEBUG: Clearing previous index...")
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)
    if os.path.exists(CHUNKS_FILE):
        os.remove(CHUNKS_FILE)
