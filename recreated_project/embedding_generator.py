import os
import json
from document_chunker import get_document_chunks
from embeddings_client import EmbeddingsClient

def generate_and_save_embeddings(output_file="embeddings.json"):
    # Hint: Do not regenerate if the file already exists
    if os.path.exists(output_file):
        print(f"Embeddings file '{output_file}' already exists. Skipping generation.")
        return

    print("Generating new embeddings... This might take a moment.")
    
    # 1. Load all chunks generated in the previous exercise
    chunks = get_document_chunks()
    
    # Initialize the client (which uses the endpoint in config.py)
    client = EmbeddingsClient()
    
    embedded_chunks = []
    
    # 2. Generate an embedding for each chunk
    for chunk in chunks:
        # Extract the text content to embed
        text_to_embed = chunk["content"]
        
        try:
            # Get the mathematical vector from the local LLM
            embedding_vector = client.get_embedding(text_to_embed)
            
            # 3. Format the result exactly as requested by the exercise
            embedded_chunk = {
                "document_id": chunk["document_id"],
                "chunk_index": chunk["chunk_index"],
                "content": chunk["content"],
                "embedding": embedding_vector
            }
            embedded_chunks.append(embedded_chunk)
            
            print(f"Successfully embedded chunk {chunk['chunk_index']} from {chunk['document_id']}")
        except Exception as e:
            print(f"Failed to embed chunk {chunk['chunk_index']}: {e}")

    # 4. Save the result into a JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(embedded_chunks, f, indent=4)
        
    print(f"\nSaved {len(embedded_chunks)} embeddings to '{output_file}'.")

# A test block to run the generation manually
if __name__ == "__main__":
    generate_and_save_embeddings()
