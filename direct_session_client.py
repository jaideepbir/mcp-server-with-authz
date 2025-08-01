#!/usr/bin/env python3
"""
Direct ClientSession test for the MCP server
"""
import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def test_server():
    """Test the MCP server using ClientSession directly"""
    print("Connecting to MCP server at http://localhost:8000/sse")
    
    try:
        async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
            # Create a client session
            session = ClientSession(read_stream, write_stream)
            
            print("[OK] Connected to server")
            
            # Initialize the session
            print("[INFO] Initializing session...")
            init_result = await session.initialize()
            print(f"[OK] Session initialized: {init_result}")
            
            # List available tools
            print("[INFO] Listing tools...")
            tools_result = await session.list_tools()
            print(f"[OK] Tools result: {tools_result}")
            
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_server())