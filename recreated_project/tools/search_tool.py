from .tool import Tool
from embeddings_client import EmbeddingsClient

# Initialize the client once to be used by the tool
client = EmbeddingsClient()

def search_company_documents(query):
    """Searches the vectorized company handbook and procedures for relevant information."""
    results = client.semantic_search(query)
    
    if not results:
        return "No relevant information found in the internal documentation."
    
    formatted_results = []
    for res in results:
        formatted_results.append(f"--- Document: {res['document_id']} ---\n{res['content']}")
        
    return "\n\n".join(formatted_results)

search_tool = Tool(
    name="search_company_documents",
    description="Searches internal company documents, handbooks, and procedures to retrieve factual information to answer user questions.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The specific search query or keyword phrase."
            }
        },
        "required": ["query"]
    },
    callback=search_company_documents
)
