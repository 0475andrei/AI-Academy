# summarizer.py
import ollama
from config import OLLAMA_MODEL

def summarize_context(messages):
    """
    Summarizes conversation history using the Ollama model from config.
    """
    to_summarize = messages[:-2]
    text_to_compress = "\n".join([m['content'] for m in to_summarize])
    
    prompt = f"Summarize the following conversation in 2-3 sentences, focusing on key security topics:\n{text_to_compress}"
    
    response = ollama.chat(
        model=OLLAMA_MODEL, 
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    return response['message']['content']