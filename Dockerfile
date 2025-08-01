# Dockerfile for MCP Server with Streamlit Client
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
RUN pip install "mcp[cli]" streamlit

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000 8501

# Default command runs the MCP server
CMD ["python", "src/mcp_server.py"]