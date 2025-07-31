#!/usr/bin/env python3
"""
Simple test for the MCP Server functions
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the functions directly
from src.mcp_server import (
    authenticate_user,
    list_tools,
    evaluate_opa_policy
)

if __name__ == "__main__":
    # Test authentication
    print("Testing authentication:")
    result = authenticate_user(username="user", password="user123")
    print(f"Authentication result: {result}")
    
    # List tools
    print("\nListing tools:")
    result = list_tools()
    print(f"Tools: {result}")
    
    # Test OPA policy evaluation
    print("\nTesting OPA policy evaluation:")
    result = evaluate_opa_policy(
        policy_name="simple",
        input_data={"user": {"role": "user"}, "action": "read"}
    )
    print(f"Policy evaluation result: {result}")