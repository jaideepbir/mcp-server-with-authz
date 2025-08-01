#!/usr/bin/env python3
"""
Robust MCP client to test the server
"""
import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.client.sse import sse_client

async def test_server():
    """Test the MCP server functionality"""
    print("Connecting to MCP server at http://localhost:8000/sse")
    
    try:
        async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
            print("[OK] Connected to server")
            
            # Send initialization request
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-01-01",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            }
            
            print("[INFO] Sending initialization request...")
            await write_stream.send(init_request)
            
            # Read the response
            print("[INFO] Waiting for response...")
            response = await asyncio.wait_for(read_stream.receive(), timeout=10.0)
            print(f"[RESPONSE] {response}")
            
    except asyncio.TimeoutError:
        print("[ERROR] Timeout waiting for server response")
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_server())