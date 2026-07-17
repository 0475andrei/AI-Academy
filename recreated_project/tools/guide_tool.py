import json
import requests
import math
from config import EMBEDDINGS_ENDPOINT, EMBEDDINGS_MODEL

def cosine_similarity(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude1 = math.sqrt(sum(a * a for a in v1))
    magnitude2 = math.sqrt(sum(b * b for b in v2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)

class CybersecGuideTool:
    def __init__(self):
        self.name = "search_metasploit_guide"
        self.description = "Searches the Metasploit documentation database to answer user questions about exploits, payloads, and commands."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The user's specific question or search term about Metasploit"
                }
            },
            "required": ["query"]
        }

    def callback(self, query):
        # 1. Embed the user's search query
        payload = {
            "model": EMBEDDINGS_MODEL,
            "input": query
        }
        
        try:
            response = requests.post(EMBEDDINGS_ENDPOINT, json=payload)
            if response.status_code != 200:
                return f"Error connecting to embedding model."
            query_vector = response.json().get("embeddings", [[]])[0]
        except Exception as e:
            return f"Connection error: {e}"

        # 2. Open the generated embeddings database
        try:
            with open("embeddings.json", "r", encoding="utf-8") as f:
                database = json.load(f)
        except FileNotFoundError:
            return "Error: Database not found. Please run the generation script first."

        # 3. Find the best matching chunk
        best_score = -1
        best_chunk = "No relevant information found."

        for chunk in database:
            score = cosine_similarity(query_vector, chunk["embedding"])
            
            if score > best_score:
                best_score = score
                best_chunk = chunk["content"]

        # 4. Return the exact paragraph to the LLM
        return f"Found relevant documentation (Relevance Score: {best_score:.2f}):\n\n{best_chunk}"