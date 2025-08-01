"""
Streamlit MCP Client Application
"""
import streamlit as st
import asyncio
import json
import aiohttp
from typing import Dict, Any, List

# Initialize session state
if 'connected' not in st.session_state:
    st.session_state.connected = False
    st.session_state.tools = []
    st.session_state.selected_tool = None
    st.session_state.tool_result = None

def initialize_session_state():
    """Initialize session state variables"""
    if 'server_url' not in st.session_state:
        st.session_state.server_url = "http://localhost:8000/sse"
    if 'tools' not in st.session_state:
        st.session_state.tools = []
    if 'selected_tool' not in st.session_state:
        st.session_state.selected_tool = None
    if 'tool_result' not in st.session_state:
        st.session_state.tool_result = None

# Set page configuration
st.set_page_config(
    page_title="MCP Client",
    page_icon="🔌",
    layout="wide"
)

# Title and description
st.title("🔌 Model Context Protocol (MCP) Client")
st.markdown("""
This application provides a user interface to interact with your MCP server.
You can list available tools, select a tool, and execute it with parameters.
""")

# Initialize session state
initialize_session_state()

# Sidebar for server connection
with st.sidebar:
    st.header("Server Connection")
    
    # Server URL input
    server_url = st.text_input(
        "MCP Server URL",
        value=st.session_state.server_url,
        help="URL of your MCP server (usually ends with /sse)"
    )
    
    # Update session state
    st.session_state.server_url = server_url
    
    # Connection status
    if st.session_state.connected:
        st.success("Connected to server")
    else:
        st.warning("Not connected")
    
    # Connect/Disconnect buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Connect", disabled=st.session_state.connected):
            st.session_state.connected = True
            st.rerun()
    with col2:
        if st.button("Disconnect", disabled=not st.session_state.connected):
            st.session_state.connected = False
            st.session_state.tools = []
            st.session_state.selected_tool = None
            st.session_state.tool_result = None
            st.rerun()

# Main content area
if not st.session_state.connected:
    st.info("👆 Please connect to your MCP server using the sidebar")
else:
    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["🔧 Tools", "ℹ️ About"])

    with tab1:
        # Tool listing and execution
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Available Tools")
            
            # Button to refresh tool list
            if st.button("🔄 Refresh Tools"):
                # In a real implementation, this would fetch tools from the server
                # For now, we'll use hardcoded tool information
                st.session_state.tools = [
                    {
                        "name": "authenticate_user",
                        "description": "Authenticate a user with username and password",
                        "parameters": {
                            "username": {"type": "string", "required": True},
                            "password": {"type": "string", "required": True}
                        }
                    },
                    {
                        "name": "list_tools",
                        "description": "List all available tools in the MCP server",
                        "parameters": {}
                    },
                    {
                        "name": "read_csv_excel",
                        "description": "Read a CSV or Excel file and return its contents as JSON",
                        "parameters": {
                            "file_path": {"type": "string", "required": True}
                        }
                    },
                    {
                        "name": "analyze_csv_excel",
                        "description": "Analyze a CSV or Excel file and return statistical summary",
                        "parameters": {
                            "file_path": {"type": "string", "required": True}
                        }
                    },
                    {
                        "name": "filter_data",
                        "description": "Filter data by column value",
                        "parameters": {
                            "file_path": {"type": "string", "required": True},
                            "column": {"type": "string", "required": True},
                            "value": {"type": "any", "required": True}
                        }
                    },
                    {
                        "name": "sort_data",
                        "description": "Sort data by column",
                        "parameters": {
                            "file_path": {"type": "string", "required": True},
                            "column": {"type": "string", "required": True},
                            "ascending": {"type": "boolean", "required": False, "default": True}
                        }
                    },
                    {
                        "name": "evaluate_opa_policy",
                        "description": "Evaluate an OPA policy with input data",
                        "parameters": {
                            "policy_name": {"type": "string", "required": True},
                            "input_data": {"type": "object", "required": True}
                        }
                    }
                ]
                st.success("Tools refreshed!")
            
            # Display tools as selectable items
            if st.session_state.tools:
                for i, tool in enumerate(st.session_state.tools):
                    if st.button(f"🔷 {tool['name']}", key=f"tool_{i}"):
                        st.session_state.selected_tool = tool
                        st.session_state.tool_result = None
                        st.rerun()
            else:
                st.info("Click 'Refresh Tools' to load available tools")
        
        with col2:
            st.subheader("Tool Execution")
            
            if st.session_state.selected_tool:
                tool = st.session_state.selected_tool
                st.markdown(f"**Selected Tool:** `{tool['name']}`")
                st.markdown(f"**Description:** {tool['description']}")
                
                # Create input fields for tool parameters
                st.markdown("**Parameters:**")
                params = {}
                
                if tool['parameters']:
                    for param_name, param_info in tool['parameters'].items():
                        required = param_info.get('required', False)
                        param_type = param_info.get('type', 'string')
                        default = param_info.get('default', None)
                        
                        label = f"{param_name} ({param_type})"
                        if required:
                            label += " *"
                            
                        if param_type == "boolean":
                            params[param_name] = st.checkbox(
                                label, 
                                value=default if default is not None else False
                            )
                        elif param_type == "integer":
                            params[param_name] = st.number_input(
                                label, 
                                value=default if default is not None else 0,
                                step=1
                            )
                        elif param_type == "number":
                            params[param_name] = st.number_input(
                                label, 
                                value=float(default) if default is not None else 0.0,
                                step=0.1
                            )
                        elif param_type == "object":
                            params[param_name] = st.text_area(
                                label, 
                                value=json.dumps(default) if default else "{}",
                                height=100
                            )
                            # Try to parse JSON
                            try:
                                params[param_name] = json.loads(params[param_name])
                            except:
                                pass
                        else:  # string and other types
                            params[param_name] = st.text_input(
                                label, 
                                value=default if default is not None else ""
                            )
                    
                    # Execute button
                    if st.button("▶️ Execute Tool", type="primary"):
                        # In a real implementation, this would call the MCP server
                        # For now, we'll simulate the response
                        st.session_state.tool_result = {
                            "tool": tool['name'],
                            "parameters": params,
                            "timestamp": "2025-08-01T12:00:00Z",
                            "result": f"This is a simulated result for tool '{tool['name']}' with parameters: {json.dumps(params, indent=2)}"
                        }
                        st.rerun()
                else:
                    st.info("This tool takes no parameters")
                    if st.button("▶️ Execute Tool", type="primary"):
                        # Simulate execution
                        st.session_state.tool_result = {
                            "tool": tool['name'],
                            "parameters": {},
                            "timestamp": "2025-08-01T12:00:00Z",
                            "result": f"This is a simulated result for tool '{tool['name']}'"
                        }
                        st.rerun()
            else:
                st.info("👈 Select a tool from the left panel to execute")
            
            # Display tool execution result
            if st.session_state.tool_result:
                st.subheader("Execution Result")
                result = st.session_state.tool_result
                st.json(result)
    
    with tab2:
        st.subheader("About MCP Client")
        st.markdown("""
        ### What is MCP?
        The Model Context Protocol (MCP) is a standardized way for applications 
        to provide context for LLMs (Large Language Models). It allows LLMs to 
        access external data sources and tools in a consistent manner.
        
        ### How to Use This Client
        1. Enter the URL of your MCP server in the sidebar
        2. Click "Connect" to establish a connection
        3. Click "Refresh Tools" to load available tools from the server
        4. Select a tool from the list
        5. Fill in the required parameters
        6. Click "Execute Tool" to run the tool
        
        ### Supported Operations
        - User authentication
        - Tool discovery
        - File processing (CSV/Excel)
        - Data analysis
        - Policy evaluation
        """)
        
        st.subheader("Server Information")
        st.info(f"Connected to: {st.session_state.server_url}")

# Footer
st.markdown("---")
st.caption("MCP Client - Connect to your Model Context Protocol server")