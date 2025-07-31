#!/usr/bin/env python3
"""
Local Agent using Gemini API to interact with MCP Server functions
"""
import os
import sys
import json
import google.generativeai as genai
from typing import Dict, Any

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import our MCP server functions
from src.mcp-server import (
    authenticate_user,
    list_tools,
    read_csv_excel,
    analyze_csv_excel,
    filter_data,
    sort_data,
    evaluate_opa_policy
)

class LocalMCPAgent:
    def __init__(self, api_key: str):
        """Initialize the agent with Gemini API key"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Define the tools available to the LLM
        self.tools = {
            "authenticate_user": self._authenticate_user,
            "list_tools": self._list_tools,
            "read_csv_excel": self._read_csv_excel,
            "analyze_csv_excel": self._analyze_csv_excel,
            "filter_data": self._filter_data,
            "sort_data": self._sort_data,
            "evaluate_opa_policy": self._evaluate_opa_policy
        }
        
        # System prompt explaining the agent's capabilities
        self.system_prompt = """
        You are an AI assistant that can interact with a Model Context Protocol (MCP) server.
        You have access to several tools that allow you to process CSV/Excel files and evaluate policies.
        
        The available tools are:
        1. authenticate_user(username, password) - Authenticate a user
        2. list_tools() - List available tools
        3. read_csv_excel(file_path) - Read a CSV or Excel file
        4. analyze_csv_excel(file_path) - Analyze a CSV or Excel file
        5. filter_data(file_path, column, value) - Filter data by column value
        6. sort_data(file_path, column, ascending) - Sort data by column
        7. evaluate_opa_policy(policy_name, input_data) - Evaluate an OPA policy
        
        When a user asks you to perform a task, use the appropriate tool and provide the result.
        Always explain what you're doing and present results in a clear format.
        """

    def _authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Wrapper for authenticate_user function"""
        return authenticate_user(username, password)

    def _list_tools(self) -> Dict[str, Any]:
        """Wrapper for list_tools function"""
        return {"tools": list_tools()}

    def _read_csv_excel(self, file_path: str) -> Dict[str, Any]:
        """Wrapper for read_csv_excel function"""
        return read_csv_excel(file_path)

    def _analyze_csv_excel(self, file_path: str) -> Dict[str, Any]:
        """Wrapper for analyze_csv_excel function"""
        return analyze_csv_excel(file_path)

    def _filter_data(self, file_path: str, column: str, value: Any) -> Dict[str, Any]:
        """Wrapper for filter_data function"""
        return filter_data(file_path, column, value)

    def _sort_data(self, file_path: str, column: str, ascending: bool = True) -> Dict[str, Any]:
        """Wrapper for sort_data function"""
        return sort_data(file_path, column, ascending)

    def _evaluate_opa_policy(self, policy_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Wrapper for evaluate_opa_policy function"""
        return evaluate_opa_policy(policy_name, input_data)

    def process_query(self, query: str) -> str:
        """Process a user query using the Gemini model and MCP tools"""
        # Start a chat session with the system prompt
        chat = self.model.start_chat(history=[
            {"role": "user", "parts": [self.system_prompt]},
            {"role": "model", "parts": ["Understood. I'm ready to help you with MCP tools."]}
        ])
        
        # Send the user query
        response = chat.send_message(query)
        
        # For simplicity, we're returning the model's response directly
        # In a more complex implementation, we would parse for tool calls
        # and execute them, then send the results back to the model
        return response.text

def main():
    """Main function to run the local agent"""
    # Get the API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        print("Please set it with: export GEMINI_API_KEY=your_api_key_here")
        return
    
    # Create the agent
    agent = LocalMCPAgent(api_key)
    
    # Example queries
    queries = [
        "List all available tools",
        "Authenticate user 'user' with password 'user123'",
        "Evaluate the simple policy for a user with role 'user' performing a 'read' action"
    ]
    
    # Process each query
    for query in queries:
        print(f"\nQuery: {query}")
        result = agent.process_query(query)
        print(f"Response: {result}")

if __name__ == "__main__":
    main()