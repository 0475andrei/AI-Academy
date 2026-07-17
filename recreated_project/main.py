import gradio as gr
import time
from agent import Agent
from llm_client import LLMClient
from conversation_context import ConversationContext
from utils import count_tokens  
from config import INPUT_TOKEN_PRICE_PER_MILLION, OUTPUT_TOKEN_PRICE_PER_MILLION
from tools.tools import tools

context = ConversationContext()
llm_client = LLMClient()
agent = Agent(llm_client, context, tools=tools)

def chat_function(message, history):
   
   
    try:
   
        start_time = time.time()
        
        """
        Handles the interaction between the user and the agent.
        """
        
        # 1. Immediate visual feedback
        yield "🛠️ *System: Checking tools for your request...*"
        
        # 2. Get the response from the agent
        response_content, tool_used = agent.process_message(message)
        
        # 3. Calculate metrics AFTER the agent has processed the message
        inputs = context.input_tokens
        outputs = context.output_tokens
        cost = (inputs / 1000000 * INPUT_TOKEN_PRICE_PER_MILLION) + (outputs / 1000000 * OUTPUT_TOKEN_PRICE_PER_MILLION)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # 4. Construct final output
        final_output = ""
        if tool_used:
            final_output += f"🛠️ *System: Tool '{tool_used}' was used to process your request.*\n\n"
        
        final_output += response_content
        
        # Add token usage as a footer
        final_output += (f"\n\n---\n"
                        f"⏱️ **Time**: {elapsed_time:.2f}s | "
                        f"📊 **Usage**: {inputs} in / {outputs} out tokens | "
                        f"💰 **Est. Cost**: ${cost:.6f}")
        
        # 5. Yield the final combined answer
        yield final_output

        
        
        print("\n--- TOKEN USAGE & COST ESTIMATION ---")
        print(f"Total cost for this conversation: ${cost:.6f} (Inputs: {inputs} tokens, Outputs: {outputs} tokens)")
        
    except Exception as e:
        print(f"❌ Gradio Chat Fatal Error: {e}")
        yield "⚠️ Sorry, I encountered a critical error. Please refresh the chat."
    
    
        
    # 6. Logging for your terminal
   
# Define the Gradio ChatInterface
demo = gr.ChatInterface(
    fn=chat_function,
    title="CYB(ri)AN - AI Cybersecurity Analyst",
    description="Ask CYBriAN about company security policies, incident protocols, or hardware procedures.",
    
    examples=["What hardware do I need to run a local server to run movies from home?", "How has AI changed cybersecurity, both for defenders and attackers?", "What are the biggest security mistakes organizations make?", "What's the most overrated cybersecurity practice?"]
)

if __name__ == "__main__":
    demo.launch()
