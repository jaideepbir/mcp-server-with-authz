#!/usr/bin/env python3
"""
Simple HTTP API tester for MCP server
"""
import requests
import json

def test_mcp_endpoints():
    """Test MCP server endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing MCP Server Endpoints")
    print("=" * 40)
    
    # Test root endpoint (should return 404)
    print("1. Testing root endpoint...")
    try:
        response = requests.get(base_url, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
    except requests.exceptions.RequestException as e:
        print(f"   Error: {e}")
    
    print("\nNote: MCP servers using SSE transport don't have traditional HTTP endpoints.")
    print("They communicate using the Model Context Protocol through SSE streams.")
    print("\nTo properly test this server, use an MCP client or the MCP Inspector tool.")

if __name__ == "__main__":
    test_mcp_endpoints()