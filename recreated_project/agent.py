import json

"""Core agent orchestration.
The agent coordinates communication between
the conversation context and the language model."""

class Agent:
    def __init__(self, llm_client, context, tools=None):
        self.llm_client = llm_client
        self.context = context
        self.tools = {tool.name: tool for tool in tools} if tools else {}

    def _handle_tool_calls(self, tool_calls):
        results = []
        for tc in tool_calls:
            tool_name = tc["function"]["name"]
            tool_id = tc["id"]
            
            try:
                # Încercăm să parsăm argumentele
                arguments_str = tc["function"]["arguments"]
                arguments = json.loads(arguments_str)
                
                # Căutăm tool-ul și îl executăm tot în interiorul try
                tool = self.tools.get(tool_name)
                if tool:
                    result = tool.callback(**arguments)
                else:
                    result = f"Tool '{tool_name}' not found"
            
            except json.JSONDecodeError:
                print(f"⚠️ Warning: Invalid JSON arguments for '{tool_name}'")
                result = "Error: Invalid JSON arguments"
            except Exception as e:
                # Prindem orice eroare la execuția callback-ului
                print(f"❌ Error executing tool '{tool_name}': {e}")
                result = f"Error: Tool execution failed: {str(e)}"

            results.append({
                "role": "tool",
                "tool_call_id": tool_id,
                "content": str(result)
            })
        return results

    def process_message(self, user_message):
        self.context.add_message({
            "role": "user",
            "content": user_message
        })

        response = self.llm_client.generate_response(
            self.context.get_history(),
            tools=list(self.tools.values())
        )

        message = response["message"]
        tool_calls = message.get("tool_calls", [])
        tool_used = None

        if tool_calls:
            self.context.add_message(message)
            tool_used = tool_calls[0]["function"]["name"] 
            # Use 'system' role for internal logs, or 'user' if you want it to appear
            # like a status update in the chat flow.
            for tc in tool_calls:
                print(f"🛠️ System: Executing tool '{tc['function']['name']}'...")
                

            tool_results = self._handle_tool_calls(tool_calls)
            for result in tool_results:
                self.context.add_message(result)

            response = self.llm_client.generate_response(
                self.context.get_history()
            )
            message = response["message"]

        self.context.add_message(message)
        return message.get("content", ""), tool_used # Return tool name
