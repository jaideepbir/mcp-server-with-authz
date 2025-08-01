# 🧩 Model Context Protocol (MCP) Server

A Model Context Protocol (MCP) server implementation with tools for data processing, authentication, and policy evaluation.

## 🔍 Overview

This project implements a Model Context Protocol (MCP) server that provides tools for:
1. User authentication with role-based access control
2. CSV/Excel reading and analysis
3. Data filtering and sorting
4. Policy evaluation using Open Policy Agent (OPA)

The server follows the Model Context Protocol specification, allowing LLMs to interact with these tools through a standardized interface.

## 🚀 Features

### ✅ Core Features
1. **Authentication**: User authentication with role-based access control
2. **Data Processing**: Read, analyze, filter, and sort CSV/Excel files
3. **Policy Evaluation**: Evaluate access control policies using Open Policy Agent
4. **Resource Access**: Access file contents through MCP resources

### ✅ Enhanced Features
1. **Streamlit Client**: User-friendly web interface to interact with all tools
2. **Specialized Tool Interfaces**:
   - File upload for CSV/Excel processing tools
   - Policy selector with predefined JSON schemas for policy evaluation
   - Role-based permissions display for authentication
3. **Docker Support**: Containerized deployment with Docker Compose
4. **Extensible Architecture**: Easy to add new tools and resources

## 📦 Prerequisites

- Python 3.8+
- pip (Python package installer)
- Git

## 🛠️ Quickstart

For detailed installation and deployment instructions, see the [Quickstart Guide](QUICKSTART.md).

### Quick Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp-server
   ```

2. Install Python dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install "mcp[cli]"
   ```

### Run the Server
```bash
python src/mcp_server.py
```
The server will be available at `http://localhost:8000` with the SSE endpoint at `http://localhost:8000/sse`.

### Run the Streamlit Client (Optional)
In a separate terminal:
```bash
streamlit run src/streamlit_mcp_client.py
```
The client will be available at `http://localhost:8501`.

## 🧪 Testing

Run the test client:
```bash
python src/mcp_client.py
```

## 📁 Project Structure

```
mcp-server/
├── src/
│   ├── mcp_server.py       # Main MCP server implementation
│   ├── streamlit_mcp_client.py # Streamlit client
│   └── mcp_client.py       # Test client
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker Compose configuration
├── QUICKSTART.md           # Quickstart and Deployment guide
└── README.md               # This file
```

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.