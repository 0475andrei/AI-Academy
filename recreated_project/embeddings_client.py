import os
import json
import requests

from config import EMBEDDINGS_MODEL, EMBEDDINGS_ENDPOINT

class EmbeddingsClient:
    def get_embedding(self, text: str) -> list[float]:
        response = requests.post(
            EMBEDDINGS_ENDPOINT,
            json={
                "model": EMBEDDINGS_MODEL,
                "input": text
            }
        )

        if not response.ok:
            print("STATUS:", response.status_code)
            print("BODY:", response.text)

        response.raise_for_status()
        return response.json()["embeddings"][0]

    def cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        """
        Computes the cosine similarity between two embedding vectors.

        Returns a float in the range [-1, 1]:
        1.0 - vectors are semantically identical
        0.0 - vectors are unrelated
        -1.0 - vectors are semantically opposite
        """
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a ** 2 for a in vec1) ** 0.5
        magnitude2 = sum(b ** 2 for b in vec2) ** 0.5
        return dot_product / (magnitude1 * magnitude2)
    
    def semantic_search(self, user_question: str, top_n: int = 3, threshold: float = 0.5):
        """
        Searches the embeddings file for chunks most relevant to the user's question.
        """
        embeddings_file = "embeddings.json"
        
        # 1. Load the chunks and embeddings generated in Exercise 4
        if not os.path.exists(embeddings_file):
            print(f"Error: {embeddings_file} not found.")
            return []
            
        try:
            with open(embeddings_file, "r", encoding="utf-8") as f:
                embedded_chunks = json.load(f)
        except Exception as e:
            print(f"Error reading embeddings: {e}")
            return []

        # 2. Generate the embedding for the user's question
        question_embedding = self.get_embedding(user_question)
        
        results = []
        
        # 3. Calculate similarity score between the question and each chunk
        for chunk in embedded_chunks:
            score = self.cosine_similarity(question_embedding, chunk["embedding"])
            
            # 5. Filter by a minimum similarity threshold
            if score >= threshold:
                results.append({
                    "document_id": chunk["document_id"],
                    "chunk_index": chunk["chunk_index"],
                    "similarity": round(score, 4),
                    "content": chunk["content"]
                })
                
        # 4. Sort results in descending order by score (highest similarity first)
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # 6. Return the top N most relevant chunks
        return results[:top_n]

# Optional: A small test block to verify your search engine works standalone
if __name__ == "__main__":
    client = EmbeddingsClient()
    test_question = "What laptop do software engineers get?"
    print(f"Searching for: '{test_question}'\n")
    
    search_results = client.semantic_search(test_question)
    
    print(json.dumps(search_results, indent=2))
