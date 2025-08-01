#!/usr/bin/env python3
"""
High-level MCP client to test the server
"""
import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp import Client
from mcp.client.sse import sse_client

async def test_server():
    """Test the MCP server using high-level client API"""
    print("Connecting to MCP server at http://localhost:8000/sse")
    
    try:
        async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
            # Create a high-level client
            client = Client(read_stream, write_stream)
            
            print("[OK] Connected to server")
            
            # Initialize the client
            print("[INFO] Initializing client...")
            await client.initialize()
            print("[OK] Client initialized")
            
            # List available tools
            print("[INFO] Listing tools...")
            tools = await client.list_tools()
            print(f"[OK] Found {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_server())