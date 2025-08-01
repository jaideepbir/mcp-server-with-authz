#!/bin/bash
# Script to run the Streamlit MCP client

echo "Starting Streamlit MCP Client..."
echo "Make sure the MCP server is running at http://localhost:8000"

# Run the Streamlit app
streamlit run src/streamlit_mcp_client.py --server.port 8501 --server.address 0.0.0.0