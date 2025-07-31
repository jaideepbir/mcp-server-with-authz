# MCP Server (Model Context Protocol)

Model Context Protocol Server with tools for data processing and policy evaluation.

## Overview

This project implements a Model Context Protocol (MCP) server that provides tools for:
1. CSV/Excel reading and analysis
2. Data filtering and sorting
3. OPA policy evaluation for access control

The server follows the Model Context Protocol specification, allowing LLMs to interact with these tools through a standardized interface.

## Features

1. **Authentication**: User authentication with role-based access control
2. **CSV/Excel Processing**: Read, analyze, filter, and sort CSV/Excel files
3. **OPA Policy Evaluation**: Evaluate access control policies (simple, advanced, attribute-based)
4. **Resource Access**: Access file contents through MCP resources
5. **Prompt Templates**: Predefined prompts for common tasks
6. **Local Agent**: Includes local agents that can interact with the MCP server using the Gemini API

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- Google Gemini API key (for local agent functionality)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp-server
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   pip install "mcp[cli]"
   pip install google-generativeai
   ```

## Running the Application

### Direct Execution
```bash
python src/mcp_server.py
```

### Development Mode (with MCP Inspector)
```bash
uv run mcp dev src/mcp_server.py
```

### As a Module
```bash
python -m src.mcp_server
```

## Running the Local Agents

### Simple Agent
```bash
export GEMINI_API_KEY=your_gemini_api_key_here
python src/gemini_agent.py
```

### Advanced Agent with Function Calling
```bash
export GEMINI_API_KEY=your_gemini_api_key_here
python src/advanced_gemini_agent.py
```

## Tools Provided

### Authentication
- `authenticate_user(username, password)`: Authenticate a user and return their role

### Tool Management
- `list_tools()`: List available tools in the MCP server

### Data Processing
- `read_csv_excel(file_path)`: Read a CSV or Excel file and return its contents as JSON
- `analyze_csv_excel(file_path)`: Analyze a CSV or Excel file and return statistical summary
- `filter_data(file_path, column, value)`: Filter data by column value
- `sort_data(file_path, column, ascending)`: Sort data by column

### Policy Evaluation
- `evaluate_opa_policy(policy_name, input_data)`: Evaluate an OPA policy with input data

## Resources

### File Access
- `file://{file_path}`: Access the content of a file

## Prompts

### Analysis Prompts
- `csv_analysis_prompt(file_path)`: Generate a prompt for CSV analysis
- `opa_policy_evaluation_prompt(policy_name, user_role, action)`: Generate a prompt for OPA policy evaluation

## Testing

Run the test client:
```bash
python src/mcp_client.py
```

## Project Structure

```
mcp-server/
├── src/
│   ├── mcp_server.py           # Main MCP server implementation
│   ├── mcp_client.py           # Test client
│   ├── gemini_agent.py         # Simple local agent using Gemini API
│   └── advanced_gemini_agent.py # Advanced local agent with function calling
├── tests/                      # Test files
├── docs/                       # Documentation
├── requirements.txt            # Python dependencies
├── package.json                # Node.js package configuration
├── playwright.config.js        # Playwright configuration
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
└── README.md                   # This file
```

## Integration with LLM Applications

This MCP server can be integrated with any LLM application that supports the Model Context Protocol, such as:
- Claude Desktop
- Custom AI applications
- IDE plugins
- Chat interfaces

It can also be used with local agents that leverage the Gemini API for natural language interaction.

## Conventional Commits

This project follows the Conventional Commits specification:
- `feat:` - New features
- `fix:` - Bug fixes
- `test:` - Adding or updating tests
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks