import tiktoken 
import os 

def count_tokens(text: str, model_name: str = "gpt-5-") -> int:
    """
    Count the number of tokens in a given text for a specific model.

    Args:
        text (str): The input text to count tokens for.
        model_name (str): The name of the model to use for tokenization. Default is "gpt-4".

    Returns:
        int: The number of tokens in the input text.
    """
    try:
        # Get the encoding for the specified model
        encoding = tiktoken.encoding_for_model(model_name)
        
        # Encode the text and return the length of the resulting token list
        tokens = encoding.encode(text)
        return len(tokens)
    
    except Exception as e:
        print(f"Error counting tokens: {e}")
        return 0
    
    
    
