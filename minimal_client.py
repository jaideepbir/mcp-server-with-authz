#!/usr/bin/env python3
"""
Minimal MCP client to test the server
"""
import asyncio
from mcp.client.sse import sse_client

async def test_connection():
    """Test basic connection to the MCP server"""
    print("Testing connection to MCP server at http://localhost:8000/sse")
    
    try:
        async with sse_client("http://localhost:8000/sse") as (server, client):
            print("[OK] Connected successfully")
            print("Initializing...")
            await client.initialize()
            print("[OK] Initialization complete")
            
            print("Listing tools...")
            tools = await client.list_tools()
            print(f"[OK] Found {len(tools)} tools")
            for tool in tools:
                print(f"  - {tool.name}")
                
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())