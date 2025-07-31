#!/bin/bash

# Setup script for MCP Server

echo "Setting up MCP Server..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file from example
echo "Creating .env file..."
cp .env.example .env

echo "Setup complete!"
echo "To start the application:"
echo "1. Start OPA: docker build -f Dockerfile.opa -t mcp-opa . && docker run -p 8181:8181 mcp-opa"
echo "2. Start server: python src/app.py"
echo "3. Start web interface: streamlit run src/web/app.py"