#!/usr/bin/env python3
"""
Very minimal MCP client to test the server connection
"""
import asyncio
from mcp.client.sse import sse_client

async def test_connection():
    """Test basic connection to the MCP server"""
    print("Testing connection to MCP server at http://localhost:8000/sse")
    
    try:
        async with sse_client("http://localhost:8000/sse") as (server, client):
            print("[OK] Connected successfully")
            print("Server object:", type(server))
            print("Client object:", type(client))
                
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())