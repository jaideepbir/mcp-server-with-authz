#!/usr/bin/env python3
"""
Simple MCP client to test the server
"""
import asyncio
import json
from mcp.client.sse import sse_client
from mcp.types import ClientCapabilities, ToolsCapability

async def test_server():
    """Test the MCP server"""
    print("Connecting to MCP server at http://localhost:8000")
    
    try:
        async with sse_client("http://localhost:8000") as (server, client):
            # Initialize connection
            print("Initializing connection...")
            await client.initialize()
            
            # List tools
            print("\nAvailable tools:")
            tools = await client.list_tools()
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Test authentication
            print("\nTesting authentication:")
            result = await client.call_tool(
                "authenticate_user",
                {"username": "user", "password": "user123"}
            )
            print(f"  Result: {json.dumps(result, indent=2)}")
            
            # List tools via tool call
            print("\nCalling list_tools tool:")
            result = await client.call_tool("list_tools")
            print(f"  Result: {json.dumps(result, indent=2)}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_server())