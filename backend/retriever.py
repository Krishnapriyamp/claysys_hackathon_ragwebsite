import numpy as np
from vector_store import model, load_index_and_chunks

def retrieve_top_k(query: str, k: int = 3) -> list:
    index, chunks = load_index_and_chunks()
    if index is None or chunks is None:
        print("DEBUG: Index or chunks not found for retrieval.")
        return []
        
    print(f"DEBUG: Retrieving top {k} chunks for query: '{query}'")
    query_embedding = model.encode([query], convert_to_numpy=True).astype('float32')
    
    actual_k = min(k, len(chunks))
    distances, indices = index.search(query_embedding, actual_k)
    
    retrieved_chunks = []
    for idx in indices[0]:
        if idx != -1 and idx < len(chunks):
            retrieved_chunks.append(chunks[idx])
            
    print(f"DEBUG: Retrieved {len(retrieved_chunks)} documents.")
    for i, doc in enumerate(retrieved_chunks):
        print(f"DEBUG: --- Doc {i+1} Preview ---")
        print(f"{doc[:150]}...")
        
    return retrieved_chunks
