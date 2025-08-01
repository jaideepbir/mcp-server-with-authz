#!/usr/bin/env python3
"""
Comprehensive test client for the MCP server
"""
import asyncio
import json
from mcp.client.stdio import stdio_client
from mcp.types import ClientCapabilities, ToolsCapability

async def test_mcp_server():
    """Test the MCP server functionality"""
    print("Testing MCP Server...")
    print("=" * 40)
    
    # Create a client connection to the server
    async with stdio_client(
        server_command=["python", "src/mcp_server.py"],
        capabilities=ClientCapabilities(
            tools=ToolsCapability(list_changes=True)
        )
    ) as (server, client):
        # Initialize the connection
        print("1. Initializing connection...")
        await client.initialize()
        print("   ✓ Connection initialized")
        
        # List available tools
        print("\n2. Listing available tools...")
        tools = await client.list_tools()
        print(f"   Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.name}")
        
        # Test authentication
        print("\n3. Testing authentication...")
        try:
            result = await client.call_tool(
                "authenticate_user", 
                {"username": "user", "password": "user123"}
            )
            print(f"   Authentication result: {result}")
        except Exception as e:
            print(f"   Error during authentication: {e}")
        
        # Test listing tools through tool call
        print("\n4. Calling list_tools tool...")
        try:
            result = await client.call_tool("list_tools")
            print(f"   Tools list: {result}")
        except Exception as e:
            print(f"   Error calling list_tools: {e}")
        
        # Test policy evaluation
        print("\n5. Testing policy evaluation...")
        try:
            result = await client.call_tool(
                "evaluate_opa_policy",
                {
                    "policy_name": "simple",
                    "input_data": {
                        "user": {"role": "user"},
                        "action": "read"
                    }
                }
            )
            print(f"   Policy evaluation result: {result}")
        except Exception as e:
            print(f"   Error during policy evaluation: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())