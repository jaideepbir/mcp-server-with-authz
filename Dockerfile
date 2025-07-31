# Dockerfile for MCP Server
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "mcp[cli]"

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run MCP server
CMD ["python", "src/mcp_server.py"]