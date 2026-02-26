import requests
from scraper import scrape_url
from chunker import chunk_text
from vector_store import create_and_save_index, clear_index
from retriever import retrieve_top_k

OLLAMA_URL = "http://localhost:11434/api/generate"
# You can change the model from 'tinyllama' to 'phi3:mini' below
OLLAMA_MODEL = "tinyllama"

def ingest_url(url: str) -> int:
    clear_index()
    text = scrape_url(url)
    if not text:
        raise ValueError("Could not extract any textual content from the URL.")
        
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    if not chunks:
        raise ValueError("Content is too short or empty, no chunks created.")
        
    num_chunks = create_and_save_index(chunks)
    return num_chunks

def answer_query(query: str) -> str:
    retrieved_chunks = retrieve_top_k(query, k=3)
    if not retrieved_chunks:
        return "Answer not found in website content."
        
    context = "\n\n".join(retrieved_chunks)
    
    prompt = f"""Use the following context to answer the user's question. If the answer is not found in the context, respond STRICTLY with "Answer not found in website content."

Context:
{context}

Question: {query}

Answer:"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        print(f"DEBUG: Sending prompt to local Ollama ({OLLAMA_MODEL})...")
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except requests.exceptions.ConnectionError:
        print("DEBUG: Connection error to Ollama. Make sure 'ollama serve' is running.")
        return "Error: Could not connect to local Ollama. Is 'ollama serve' running?"
    except Exception as e:
        print(f"DEBUG: Error querying Ollama: {e}")
        return f"Error interacting with local LLM: {str(e)}"
