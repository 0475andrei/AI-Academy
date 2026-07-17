import os
import json
from config import CHUNK_SIZE

def get_document_chunks():
    """
    Loads documents marked with "always_load": false and splits them into fixed-size chunks.
    """
    base_dir = "knowledge"
    sub_dirs = ["facts", "procedures"]
    all_chunks = []

    for sub_dir in sub_dirs:
        registry_path = os.path.join(base_dir, sub_dir, "registry.json")
        
        # Skip if the registry doesn't exist
        if not os.path.exists(registry_path):
            continue
            
        with open(registry_path, 'r', encoding='utf-8') as f:
            try:
                registry = json.load(f)
            except json.JSONDecodeError:
                continue
                
        # Iterate through the registry to find documents that should NOT be loaded into the prompt
        for item in registry:
            if item.get("always_load") is False:
                doc_id = item["id"]
                file_path = os.path.join(base_dir, sub_dir, f"{doc_id}.md")
                
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as doc_file:
                        content = doc_file.read()
                        
                    # --- CHUNKING LOGIC ---
                    current_position = 0
                    chunk_index = 0
                    
                    # Loop through the text, slicing it into chunks of CHUNK_SIZE
                    while current_position < len(content):
                        # Extract the slice of text
                        chunk_text = content[current_position : current_position + CHUNK_SIZE]
                        
                        # Save the formatted dictionary
                        all_chunks.append({
                            "document_id": doc_id,
                            "chunk_index": chunk_index,
                            "content": chunk_text.strip()
                        })
                        
                        # Move the position forward for the next chunk
                        current_position += CHUNK_SIZE
                        chunk_index += 1

    return all_chunks

# Optional: A small test block to verify it works if you run this file directly
if __name__ == "__main__":
    chunks = get_document_chunks()
    print(f"Total chunks generated: {len(chunks)}")
    if chunks:
        print("\nPreview of the first chunk:")
        print(json.dumps(chunks[0], indent=2))
