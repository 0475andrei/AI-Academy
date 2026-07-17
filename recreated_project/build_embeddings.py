# Create this as build_embeddings.py in your project folder
import json
from document_chunker import get_document_chunks
import requests
from config import EMBEDDINGS_ENDPOINT, EMBEDDINGS_MODEL

def build():
    chunks = get_document_chunks()
    print(f"Generating embeddings for {len(chunks)} chunks...")
    
    for chunk in chunks:
        payload = {"model": EMBEDDINGS_MODEL, "input": chunk["content"]}
        response = requests.post(EMBEDDINGS_ENDPOINT, json=payload)
        if response.status_code == 200:
            chunk["embedding"] = response.json().get("embeddings", [[]])[0]
        else:
            print(f"Error embedding chunk {chunk['chunk_index']}")
    
    with open("embeddings.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4)
    print("Successfully built embeddings.json!")

if __name__ == "__main__":
    build()