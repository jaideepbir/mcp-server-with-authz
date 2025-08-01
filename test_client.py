#!/usr/bin/env python3
"""
Simple client to test the MCP server
"""
import asyncio
import json
from mcp.client.sse import sse_client
from mcp.types import ClientCapabilities, ToolsCapability

async def main():
    async with sse_client(
        "http://localhost:8000",
        capabilities=ClientCapabilities(
            tools=ToolsCapability(list_changes=True)
        )
    ) as (server, client):
        # Initialize the connection
        await client.initialize()
        
        # List available tools
        print("Available tools:")
        tools = await client.list_tools()
        for tool in tools:
            print(f"  - {tool.name}")
        
        # Test authentication
        print("\nTesting authentication:")
        result = await client.call_tool("authenticate_user", {"username": "user", "password": "user123"})
        print(f"Authentication result: {result}")
        
        # List tools again
        print("\nListing tools:")
        result = await client.call_tool("list_tools")
        print(f"Tools: {result}")

if __name__ == "__main__":
    asyncio.run(main())