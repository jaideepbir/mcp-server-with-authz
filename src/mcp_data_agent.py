#!/usr/bin/env python3
"""
MCP Data Agent for Google ADK Web Interface
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.function_tool import FunctionTool
from src.mcp_adk_tools import (
    authenticate_user,
    list_tools,
    read_csv_excel,
    analyze_csv_excel,
    filter_data,
    sort_data,
    evaluate_opa_policy
)

def create_agent():
    """Create and return the MCP data agent"""
    # Create FunctionTool instances for each function
    tools = [
        FunctionTool(authenticate_user),
        FunctionTool(list_tools),
        FunctionTool(read_csv_excel),
        FunctionTool(analyze_csv_excel),
        FunctionTool(filter_data),
        FunctionTool(sort_data),
        FunctionTool(evaluate_opa_policy),
    ]

    # Set names and descriptions for the tools
    tools[0].name = "authenticate_user"
    tools[0].description = "Authenticate a user with username and password"

    tools[1].name = "list_tools"
    tools[1].description = "List all available tools"

    tools[2].name = "read_csv_excel"
    tools[2].description = "Read a CSV or Excel file and return its contents"

    tools[3].name = "analyze_csv_excel"
    tools[3].description = "Analyze a CSV or Excel file and return statistical summary"

    tools[4].name = "filter_data"
    tools[4].description = "Filter data by column value"

    tools[5].name = "sort_data"
    tools[5].description = "Sort data by column"

    tools[6].name = "evaluate_opa_policy"
    tools[6].description = "Evaluate an OPA policy with input data"

    # Create an LLM agent with all the tools
    agent = LlmAgent(
        name="mcp_data_agent",
        description="An agent that provides tools for data processing and policy evaluation",
        tools=tools
    )
    
    return agent

# For ADK to be able to import and use the agent
agent = create_agent()

if __name__ == "__main__":
    # If run directly, print agent info
    print("MCP Data Agent")
    print("=" * 20)
    print(f"Name: {agent.name}")
    print(f"Description: {agent.description}")
    print("\nAvailable tools:")
    for tool in agent.tools:
        print(f"  - {tool.name}: {tool.description}")