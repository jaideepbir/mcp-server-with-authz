#!/usr/bin/env python3
"""
Simple test for the MCP Server
"""
from src.mcp_server import mcp

# Test the server functions directly
if __name__ == "__main__":
    # Test authentication
    print("Testing authentication:")
    result = mcp._tools["authenticate_user"].function(username="user", password="user123")
    print(f"Authentication result: {result}")
    
    # List tools
    print("\nListing tools:")
    result = mcp._tools["list_tools"].function()
    print(f"Tools: {result}")
    
    # Test OPA policy evaluation
    print("\nTesting OPA policy evaluation:")
    result = mcp._tools["evaluate_opa_policy"].function(
        policy_name="simple",
        input_data={"user": {"role": "user"}, "action": "read"}
    )
    print(f"Policy evaluation result: {result}")