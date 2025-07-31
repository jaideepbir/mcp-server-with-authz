#!/usr/bin/env python3
"""
Advanced Local Agent using Gemini API with function calling capability
"""
import os
import sys
import json
import google.generativeai as genai
from typing import Dict, Any, List, Optional, Callable
import re

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

class AdvancedMCPAgent:
    def __init__(self, api_key: str):
        """Initialize the agent with Gemini API key"""
        genai.configure(api_key=api_key)
        
        # Define the tools available to the LLM with their schemas
        self.tools = [
            {
                "name": "authenticate_user",
                "description": "Authenticate a user with username and password",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string", "description": "Username"},
                        "password": {"type": "string", "description": "Password"}
                    },
                    "required": ["username", "password"]
                }
            },
            {
                "name": "list_tools",
                "description": "List all available tools",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "read_csv_excel",
                "description": "Read a CSV or Excel file and return its contents",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to the CSV or Excel file"}
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "analyze_csv_excel",
                "description": "Analyze a CSV or Excel file and return statistical summary",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to the CSV or Excel file"}
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "filter_data",
                "description": "Filter data by column value",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to the CSV or Excel file"},
                        "column": {"type": "string", "description": "Column name to filter by"},
                        "value": {"type": ["string", "number"], "description": "Value to filter by"}
                    },
                    "required": ["file_path", "column", "value"]
                }
            },
            {
                "name": "sort_data",
                "description": "Sort data by column",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to the CSV or Excel file"},
                        "column": {"type": "string", "description": "Column name to sort by"},
                        "ascending": {"type": "boolean", "description": "Sort order (true for ascending)", "default": True}
                    },
                    "required": ["file_path", "column"]
                }
            },
            {
                "name": "evaluate_opa_policy",
                "description": "Evaluate an OPA policy with input data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "policy_name": {"type": "string", "description": "Name of the policy to evaluate"},
                        "input_data": {"type": "object", "description": "Input data for policy evaluation"}
                    },
                    "required": ["policy_name", "input_data"]
                }
            }
        ]
        
        # Map tool names to actual functions
        self.tool_functions = {
            "authenticate_user": authenticate_user,
            "list_tools": list_tools,
            "read_csv_excel": read_csv_excel,
            "analyze_csv_excel": analyze_csv_excel,
            "filter_data": filter_data,
            "sort_data": sort_data,
            "evaluate_opa_policy": evaluate_opa_policy
        }
        
        # System prompt explaining the agent's capabilities
        self.system_prompt = """
        You are an AI assistant that can interact with a Model Context Protocol (MCP) server.
        You have access to several tools that allow you to process CSV/Excel files and evaluate policies.
        
        When a user asks you to perform a task, determine which tool to use and provide the required parameters.
        Format your tool calls as JSON objects with a "tool" field and a "parameters" field.
        
        Example:
        {
          "tool": "authenticate_user",
          "parameters": {
            "username": "user",
            "password": "user123"
          }
        }
        
        After calling a tool, I will provide you with the result. Use that information to answer the user's query.
        Always explain what you're doing and present results in a clear format.
        """

    def execute_tool(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call"""
        tool_name = tool_call.get("tool")
        parameters = tool_call.get("parameters", {})
        
        if tool_name not in self.tool_functions:
            return {"error": f"Unknown tool: {tool_name}"}
        
        try:
            result = self.tool_functions[tool_name](**parameters)
            return {"tool": tool_name, "result": result}
        except Exception as e:
            return {"tool": tool_name, "error": str(e)}

    def extract_tool_calls(self, text: str) -> List[Dict[str, Any]]:
        """Extract tool calls from the model's response"""
        # Look for JSON objects that contain tool calls
        tool_calls = []
        # Pattern to match JSON objects with tool and parameters fields
        pattern = r'\{[^}]*"tool"[^}]*"parameters"[^}]*\}'
        
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                tool_call = json.loads(match)
                if "tool" in tool_call and "parameters" in tool_call:
                    tool_calls.append(tool_call)
            except json.JSONDecodeError:
                continue
        
        return tool_calls

    def process_query(self, query: str) -> str:
        """Process a user query using the Gemini model and MCP tools"""
        # Start a chat session with the system prompt
        model = genai.GenerativeModel(
            'gemini-1.5-pro-latest',
            generation_config={"response_mime_type": "text/plain"}
        )
        
        chat = model.start_chat(history=[
            {"role": "user", "parts": [self.system_prompt]},
            {"role": "model", "parts": ["Understood. I'm ready to help you with MCP tools. Please tell me what you'd like to do."]}
        ])
        
        # Send the user query
        response = chat.send_message(query)
        response_text = response.text
        
        # Extract and execute tool calls
        tool_calls = self.extract_tool_calls(response_text)
        if tool_calls:
            results = []
            for tool_call in tool_calls:
                result = self.execute_tool(tool_call)
                results.append(result)
            
            # Send the results back to the model
            results_text = json.dumps(results, indent=2)
            followup = chat.send_message(f"Tool execution results:\n{results_text}")
            return followup.text
        else:
            return response_text

def main():
    """Main function to run the local agent"""
    # Get the API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        print("Please set it with: export GEMINI_API_KEY=your_api_key_here")
        return
    
    # Create the agent
    agent = AdvancedMCPAgent(api_key)
    
    # Create a sample CSV file for testing
    sample_csv = """name,age,department,salary
John Doe,30,Engineering,75000
Jane Smith,25,Marketing,65000
Bob Johnson,35,Sales,70000
Alice Brown,28,Engineering,80000
Charlie Wilson,40,Management,90000"""
    
    with open("sample_data.csv", "w") as f:
        f.write(sample_csv)
    
    print("Sample CSV file created: sample_data.csv")
    
    # Example queries
    queries = [
        "List all available tools",
        "Authenticate user 'user' with password 'user123'",
        "Read the sample_data.csv file",
        "Analyze the sample_data.csv file",
        "Evaluate the simple policy for a user with role 'user' performing a 'read' action"
    ]
    
    # Process each query
    for query in queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print('='*50)
        result = agent.process_query(query)
        print(f"Response:\n{result}")

if __name__ == "__main__":
    main()