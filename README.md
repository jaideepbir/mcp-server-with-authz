# MCP Server

Multi-Component Platform Server with authenticated tools for data processing and policy evaluation.

## Features

1. **Authentication**: JWT-based authentication for all tools
2. **CSV/Excel Reader**: Read and display CSV/Excel files
3. **CSV/Excel Analyzer**: Analyze data and generate visualizations with Plotly
4. **OPA Client**: Evaluate access control policies using Open Policy Agent
5. **Streamlit Web Interface**: User-friendly interface to access all tools
6. **API Documentation**: Swagger-like API documentation

## Prerequisites

- Python 3.8+
- Docker (for OPA service)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp-server
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (copy `.env.example` to `.env` and modify as needed):
   ```bash
   cp .env.example .env
   ```

## Running the Application

1. Start the OPA service:
   ```bash
   docker build -f Dockerfile.opa -t mcp-opa .
   docker run -p 8181:8181 mcp-opa
   ```

2. Start the MCP server:
   ```bash
   python src/app.py
   ```

3. Start the Streamlit web interface:
   ```bash
   streamlit run src/web/app.py
   ```

## API Endpoints

### Authentication
- `POST /api/auth/login` - Generate JWT token

### CSV/Excel Reader
- `POST /api/csv-reader/read` - Read CSV/Excel file

### CSV/Excel Analyzer
- `POST /api/csv-analyzer/analyze` - Analyze CSV/Excel file
- `POST /api/csv-analyzer/visualize` - Generate visualization from CSV/Excel data

### OPA Client
- `GET /api/opa/policies` - List available policies
- `POST /api/opa/evaluate` - Evaluate policy with input data

## Testing

Run tests with:
```bash
python -m pytest tests/
```

## Project Structure

```
mcp-server/
├── src/
│   ├── app.py              # Main application
│   ├── auth/               # Authentication module
│   ├── tools/              # Tool implementations
│   │   ├── csv_reader.py   # CSV/Excel reader
│   │   ├── csv_analyzer.py # CSV/Excel analyzer
│   │   └── opa_client.py   # OPA client
│   └── web/                # Streamlit web interface
│       └── app.py
├── policies/               # OPA policies
├── tests/                  # Test files
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
├── Dockerfile.opa          # OPA Dockerfile
└── README.md               # This file
```

## Policies

The OPA client includes three sample policies:

1. **Simple**: Basic role-based access control
2. **Advanced**: Department-based access control
3. **Attribute-based**: Clearance-level and group-based access control

Each policy has corresponding test cases in the tests directory.