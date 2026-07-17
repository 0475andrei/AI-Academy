"""
Conversation memory management.
This module is responsible for storing and retrieving
messages exchanged between the user and the AI assistant.
"""
import os
import json
from summarizer import summarize_context
from utils import count_tokens
from config import MAX_TOKENS

class ConversationContext:
    def __init__(self):
        self.messages = [
            self.assemble_system_prompt()
        ]
        self.max_tokens = MAX_TOKENS
        self.input_tokens = 0
        self.output_tokens = 0
        
        # Calculate initial tokens for system prompt
        self.input_tokens += count_tokens(self.messages[0]['content'])
        
    def compress_context(self):
        """
        Compresses conversation history using an external summarizer,
        keeping the system prompt and the last 2 messages intact.
        """
        # Keep System Prompt (idx 0) and the last 2 messages (context-critical)
        if len(self.messages) > 5:
            system_prompt = self.messages[0]
            to_compress = self.messages[1:-2]
            recent_messages = self.messages[-2:]
            
            # Generate summary via modular component
            summary = summarize_context(to_compress)
            
            # Rebuild history
            self.messages = [
                system_prompt,
                {"role": "system", "content": f"PREVIOUS CONVERSATION SUMMARY: {summary}"}
            ] + recent_messages
            
            print("\n--- Context compressed using local Ollama model ---")

    def _read_file(self, filepath):
        """Helper function to safely read text from a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"⚠️ Warning: File not found: {filepath}")
            return "[Error: System document missing.]"
        except PermissionError:
            print(f"⚠️ Warning: Permission denied: {filepath}")
            return "[Error: System document inaccessible.]"
        except Exception as e:
            print(f"⚠️ Unexpected error reading {filepath}: {str(e)}")
            return "[Error: Document system error.]"

    def _load_registry(self, folder_path):
        """Helper function to load a registry.json file."""
        registry_path = os.path.join(folder_path, "registry.json")
        if not os.path.exists(registry_path):
            return []
        
        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading registry at {registry_path}: {e}")
            return []

    def assemble_system_prompt(self):
        system_prompt_parts = []
        base_dir = "knowledge"

        # 1. Load Prompts (Identity)
        identity_path = os.path.join(base_dir, "prompts", "identity.md")
        if os.path.exists(identity_path):
            identity_text = self._read_file(identity_path)
            system_prompt_parts.append(f"# Agent Identity\n{identity_text}")

        # 2. Load Facts & Procedures
        for folder in ["facts", "procedures"]:
            dir_path = os.path.join(base_dir, folder)
            registry = self._load_registry(dir_path)
            for item in registry:
                if item.get("always_load") is True:
                    file_path = os.path.join(dir_path, f"{item['id']}.md")
                    content = self._read_file(file_path)
                    system_prompt_parts.append(f"# {item['name']}\n{content}")

        final_prompt = "\n\n".join(system_prompt_parts)
        return {"role": "system", "content": final_prompt}

    def add_message(self, message):
        self.messages.append(message)
        content = message.get('content') or ""
        tokens = count_tokens(content) # Ensure your count_tokens doesn't force a model name if not needed
        
        if message.get('role') == 'assistant':
            self.output_tokens += tokens
        else:
            self.input_tokens += tokens

    def get_history(self):
        total_tokens = self.input_tokens + self.output_tokens
        if total_tokens > self.max_tokens:
            self.compress_context()
        
        return self.messages