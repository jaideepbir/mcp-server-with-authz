"""
ADK App Configuration
"""
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.function_tool import FunctionTool
from src.mcp_adk_tools import (
    authenticate_user,
    list_tools,
    read_csv_excel,
    analyze_csv_excel,
    filter_data,
    sort_data,
    evaluate_opa_policy
)

# Create FunctionTool instances for each function
tools = [
    FunctionTool(authenticate_user),
    FunctionTool(list_tools),
    FunctionTool(read_csv_excel),
    FunctionTool(analyze_csv_excel),
    FunctionTool(filter_data),
    FunctionTool(sort_data),
    FunctionTool(evaluate_opa_policy),
]

# Set names and descriptions for the tools
tools[0].name = "authenticate_user"
tools[0].description = "Authenticate a user with username and password"

tools[1].name = "list_tools"
tools[1].description = "List all available tools"

tools[2].name = "read_csv_excel"
tools[2].description = "Read a CSV or Excel file and return its contents"

tools[3].name = "analyze_csv_excel"
tools[3].description = "Analyze a CSV or Excel file and return statistical summary"

tools[4].name = "filter_data"
tools[4].description = "Filter data by column value"

tools[5].name = "sort_data"
tools[5].description = "Sort data by column"

tools[6].name = "evaluate_opa_policy"
tools[6].description = "Evaluate an OPA policy with input data"

# Create an LLM agent with all the tools
agent = LlmAgent(
    name="mcp_data_agent",
    description="An agent that provides tools for data processing and policy evaluation",
    tools=tools
)

# ADK expects an 'app' object
app = agent