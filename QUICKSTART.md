# Quickstart & Deployment Guide

## Quickstart

1. **Prerequisites**
   - Python 3.8+
   - Git
   - Docker and Docker Compose (optional, for containerized deployment)

2. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd mcp-server
   ```

3. **Install Dependencies**
   Create a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install "mcp[cli]"
   ```

4. **Run the MCP Server**
   ```bash
   python src/mcp_server.py
   ```
   The server will be available at `http://localhost:8000` with the SSE endpoint at `http://localhost:8000/sse`.

5. **Run the Streamlit Client (Optional)**
   In a separate terminal:
   ```bash
   streamlit run src/streamlit_mcp_client.py
   ```
   The client will be available at `http://localhost:8501`.

## Deployment

### Option 1: Docker Compose (Recommended)
This option deploys both the MCP server and Streamlit client in separate containers.

1. **Build and Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the Services**
   - MCP Server: `http://localhost:8000/sse`
   - Streamlit Client: `http://localhost:8501`

3. **Stop the Services**
   ```bash
   docker-compose down
   ```

### Option 2: Manual Deployment
This option manually installs and runs the services on your system.

1. **Install Dependencies**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install "mcp[cli]"
   ```

2. **Run the Services**
   ```bash
   # Terminal 1 - Run MCP Server
   python src/mcp_server.py
   
   # Terminal 2 - Run Streamlit Client (optional)
   streamlit run src/streamlit_mcp_client.py
   ```

### Option 3: Deploy to Cloud Platform
This option deploys the services to a cloud platform like AWS, Azure, or GCP.

1. **Prepare for Cloud Deployment**
   - Create a cloud account and set up authentication
   - Package the application code:
     ```bash
     zip -r mcp-server.zip src/ requirements.txt
     ```

2. **Deploy to Cloud Platform**
   - Follow the specific deployment instructions for your cloud platform:
     - AWS Elastic Beanstalk: https://aws.amazon.com/elasticbeanstalk/
     - Azure App Service: https://azure.microsoft.com/en-us/services/app-service/
     - Google Cloud Run: https://cloud.google.com/run

## Configuration

### Environment Variables
The MCP server supports the following environment variables:

- `HOST`: Bind address for the server (default: `0.0.0.0`)
- `PORT`: Port for the server (default: `8000`)

Example:
```bash
export HOST=0.0.0.0
export PORT=8000
python src/mcp_server.py
```

### Docker Environment
When using Docker, you can set environment variables in the `docker-compose.yml` file:

```yaml
environment:
  - HOST=0.0.0.0
  - PORT=8000
```

## Testing

### Unit Tests
Run the unit tests:
```bash
python -m pytest tests/
```

### Integration Tests
Run the integration tests:
```bash
python -m pytest tests/integration_tests/
```

### Manual Testing
1. Start the MCP server:
   ```bash
   python src/mcp_server.py
   ```
2. Start the Streamlit client:
   ```bash
   streamlit run src/streamlit_mcp_client.py
   ```
3. Open your browser and navigate to `http://localhost:8501`
4. Connect to the MCP server at `http://localhost:8000/sse`
5. Test each tool using the enhanced interfaces:
   - **Authentication**: Use predefined admin (`admin/admin123`) or user (`user/user123`) credentials
   - **File Processing**: Upload CSV or Excel files to test reading, analyzing, filtering, and sorting
   - **Policy Evaluation**: Select predefined policies and configure parameters

## Troubleshooting

### Server Won't Start
1. Check if the port is already in use:
   ```bash
   lsof -i :8000
   ```
2. Kill the process using the port if necessary:
   ```bash
   kill -9 <PID>
   ```

### Client Can't Connect to Server
1. Verify the server is running:
   ```bash
   curl -I http://localhost:8000/sse
   ```
2. Check if the server URL is correct in the client:
   - In the Streamlit client: Verify the URL in the sidebar
   - In custom clients: Ensure the SSE endpoint URL is correct (should end with `/sse`)

### Docker Issues
1. Check if Docker is running:
   ```bash
   docker info
   ```
2. Restart Docker if necessary:
   ```bash
   sudo systemctl restart docker
   ```

### Authentication Failures
1. Verify credentials:
   - Admin user: `admin` / `admin123`
   - Regular user: `user` / `user123`
2. Check if the user exists in the `USERS` dictionary in `src/mcp_server.py`

## Support

For questions or issues, please:
1. Check the [GitHub Issues](https://github.com/<REPO>/issues)
2. Create a new issue if needed
3. Contact the development team at [email@example.com]