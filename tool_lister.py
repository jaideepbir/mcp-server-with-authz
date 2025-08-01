#!/usr/bin/env python3
"""
Working MCP client to list tools and their descriptions
"""
import asyncio
import json
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def list_mcp_tools():
    """Connect to the MCP server and list all available tools"""
    print("Connecting to MCP server at http://localhost:8000/sse")
    print("=" * 50)
    
    try:
        async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
            # Create a client session
            session = ClientSession(read_stream, write_stream)
            
            print("[OK] Connected to server")
            
            # Initialize the session
            print("\nInitializing session...")
            init_result = await session.initialize()
            print("[OK] Session initialized")
            
            # List available tools
            print("\nListing available tools...")
            tools_result = await session.list_tools()
            
            print(f"\nFound {len(tools_result.tools)} tools:")
            print("-" * 30)
            
            for i, tool in enumerate(tools_result.tools, 1):
                print(f"{i}. {tool.name}")
                if tool.description:
                    print(f"   Description: {tool.description}")
                if tool.input_schema:
                    print(f"   Input Schema: {json.dumps(tool.input_schema, indent=2)}")
                print()
                
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        # Print full traceback for debugging
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(list_mcp_tools())