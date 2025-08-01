"""
Streamlit MCP Client Application
"""
import streamlit as st
import asyncio
import json
import tempfile
import os
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
                
                # Enhanced UI for specific tools
                if tool['name'] == 'authenticate_user':
                    st.markdown("**Enhanced Authentication Interface**")
                    
                    # Predefined user options
                    user_type = st.radio(
                        "Select User Type:",
                        ["Regular User", "Administrator"],
                        horizontal=True
                    )
                    
                    if user_type == "Regular User":
                        username = "user"
                        password = "user123"
                        st.info("Regular User Permissions: Read-only access to data processing tools")
                    else:
                        username = "admin"
                        password = "admin123"
                        st.info("Administrator Permissions: Full access to all tools and data processing capabilities")
                    
                    # Show credentials (in a real app, these would be hidden)
                    st.text_input("Username", value=username, key="auth_username", disabled=True)
                    st.text_input("Password", value=password, type="password", key="auth_password", disabled=True)
                    
                    if st.button("🔒 Authenticate", type="primary"):
                        # Simulate authentication result
                        if username == "admin":
                            st.session_state.tool_result = {
                                "tool": "authenticate_user",
                                "parameters": {"username": username, "password": password},
                                "timestamp": "2025-08-01T12:00:00Z",
                                "result": {
                                    "authenticated": True,
                                    "username": username,
                                    "role": "admin",
                                    "permissions": [
                                        "Full access to all tools",
                                        "Read/write access to all data",
                                        "Policy administration privileges",
                                        "User management capabilities"
                                    ]
                                }
                            }
                        else:
                            st.session_state.tool_result = {
                                "tool": "authenticate_user",
                                "parameters": {"username": username, "password": password},
                                "timestamp": "2025-08-01T12:00:00Z",
                                "result": {
                                    "authenticated": True,
                                    "username": username,
                                    "role": "user",
                                    "permissions": [
                                        "Read-only access to data processing tools",
                                        "Execute analysis functions",
                                        "View policy evaluations"
                                    ]
                                }
                            }
                        st.rerun()
                
                elif tool['name'] in ['read_csv_excel', 'analyze_csv_excel']:
                    st.markdown("**Enhanced File Processing Interface**")
                    
                    # File uploader
                    uploaded_file = st.file_uploader(
                        "Upload CSV or Excel File",
                        type=["csv", "xlsx", "xls"],
                        key=f"file_uploader_{tool['name']}"
                    )
                    
                    if uploaded_file is not None:
                        # Save file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            temp_file_path = tmp_file.name
                        
                        st.success(f"File uploaded: {uploaded_file.name}")
                        st.info(f"Temporary path: {temp_file_path}")
                        
                        # Parameter input
                        params = {
                            "file_path": temp_file_path
                        }
                        
                        if st.button(f"📄 {tool['name'].replace('_', ' ').title()}", type="primary"):
                            # Simulate file processing
                            st.session_state.tool_result = {
                                "tool": tool['name'],
                                "parameters": params,
                                "timestamp": "2025-08-01T12:00:00Z",
                                "result": f"Processed file: {uploaded_file.name}"
                            }
                            st.rerun()
                        
                        # Clean up temp file
                        if os.path.exists(temp_file_path):
                            os.unlink(temp_file_path)
                    else:
                        st.info("Please upload a CSV or Excel file to process")
                
                elif tool['name'] == 'evaluate_opa_policy':
                    st.markdown("**Enhanced Policy Evaluation Interface**")
                    
                    # Policy selector
                    policy_options = {
                        "Simple Policy": "simple",
                        "Advanced Policy": "advanced",
                        "Attribute-Based Policy": "attribute_based"
                    }
                    
                    selected_policy_label = st.selectbox(
                        "Select Policy:",
                        list(policy_options.keys())
                    )
                    
                    selected_policy = policy_options[selected_policy_label]
                    
                    # Preload policy-specific JSON schema
                    if selected_policy == "simple":
                        st.markdown("**Simple Policy Schema:**")
                        st.json({
                            "user": {"role": "string"},
                            "action": "string"
                        })
                        
                        # Predefined inputs for simple policy
                        user_role = st.selectbox("User Role:", ["admin", "user"])
                        action = st.selectbox("Action:", ["read", "write", "delete"])
                        
                        input_data = {
                            "user": {"role": user_role},
                            "action": action
                        }
                        
                    elif selected_policy == "advanced":
                        st.markdown("**Advanced Policy Schema:**")
                        st.json({
                            "user": {
                                "role": "string",
                                "department": "string"
                            },
                            "document": {
                                "department": "string"
                            },
                            "action": "string"
                        })
                        
                        # Predefined inputs for advanced policy
                        user_role = st.selectbox("User Role:", ["admin", "user"], key="adv_role")
                        user_dept = st.text_input("User Department:", "Engineering", key="user_dept")
                        doc_dept = st.text_input("Document Department:", "Engineering", key="doc_dept")
                        action = st.selectbox("Action:", ["read", "write", "delete"], key="adv_action")
                        
                        input_data = {
                            "user": {
                                "role": user_role,
                                "department": user_dept
                            },
                            "document": {
                                "department": doc_dept
                            },
                            "action": action
                        }
                        
                    else:  # attribute_based
                        st.markdown("**Attribute-Based Policy Schema:**")
                        st.json({
                            "user": {
                                "role": "string",
                                "clearance_level": "integer"
                            },
                            "document": {
                                "classification_level": "integer"
                            }
                        })
                        
                        # Predefined inputs for attribute-based policy
                        user_role = st.selectbox("User Role:", ["admin", "user"], key="attr_role")
                        clearance = st.slider("User Clearance Level:", 0, 10, 5, key="clearance")
                        classification = st.slider("Document Classification Level:", 0, 10, 3, key="classification")
                        
                        input_data = {
                            "user": {
                                "role": user_role,
                                "clearance_level": clearance
                            },
                            "document": {
                                "classification_level": classification
                            }
                        }
                    
                    st.markdown("**Input Data Preview:**")
                    st.json(input_data)
                    
                    if st.button("🛡️ Evaluate Policy", type="primary"):
                        # Simulate policy evaluation
                        st.session_state.tool_result = {
                            "tool": "evaluate_opa_policy",
                            "parameters": {
                                "policy_name": selected_policy,
                                "input_data": input_data
                            },
                            "timestamp": "2025-08-01T12:00:00Z",
                            "result": {
                                "allowed": True if input_data.get("user", {}).get("role") == "admin" else False,
                                "policy": selected_policy,
                                "input": input_data
                            }
                        }
                        st.rerun()
                
                elif tool['name'] in ['filter_data', 'sort_data']:
                    st.markdown("**Enhanced Data Processing Interface**")
                    
                    # File path input
                    file_path = st.text_input(
                        "File Path:",
                        placeholder="/path/to/your/file.csv",
                        help="Enter the path to your CSV or Excel file"
                    )
                    
                    if file_path:
                        if tool['name'] == 'filter_data':
                            # Filter-specific inputs
                            column = st.text_input("Column to Filter By:", "name")
                            value = st.text_input("Filter Value:", "John")
                            
                            params = {
                                "file_path": file_path,
                                "column": column,
                                "value": value
                            }
                            
                        else:  # sort_data
                            # Sort-specific inputs
                            column = st.text_input("Column to Sort By:", "age")
                            ascending = st.checkbox("Ascending Order", value=True)
                            
                            params = {
                                "file_path": file_path,
                                "column": column,
                                "ascending": ascending
                            }
                        
                        if st.button(f"📊 {tool['name'].replace('_', ' ').title()}", type="primary"):
                            # Simulate data processing
                            st.session_state.tool_result = {
                                "tool": tool['name'],
                                "parameters": params,
                                "timestamp": "2025-08-01T12:00:00Z",
                                "result": f"Processed data with parameters: {json.dumps(params, indent=2)}"
                            }
                            st.rerun()
                    else:
                        st.info("Please enter a file path to process")
                
                elif tool['name'] == 'list_tools':
                    st.markdown("**Tool Listing Interface**")
                    
                    if st.button("📋 List Available Tools", type="primary"):
                        # Simulate tool listing
                        st.session_state.tool_result = {
                            "tool": "list_tools",
                            "parameters": {},
                            "timestamp": "2025-08-01T12:00:00Z",
                            "result": [
                                "authenticate_user",
                                "list_tools", 
                                "read_csv_excel",
                                "analyze_csv_excel",
                                "filter_data",
                                "sort_data",
                                "evaluate_opa_policy"
                            ]
                        }
                        st.rerun()
                
                else:
                    # Generic parameter input for other tools
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
                            # Simulate execution
                            st.session_state.tool_result = {
                                "tool": tool['name'],
                                "parameters": params,
                                "timestamp": "2025-08-01T12:00:00Z",
                                "result": f"Executed tool '{tool['name']}' with parameters: {json.dumps(params, indent=2)}"
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
                                "result": f"Executed tool '{tool['name']}'"
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
        
        ### Enhanced Tool Interfaces
        - **Authentication**: Predefined user credentials with role-based permissions display
        - **File Processing**: File upload interface for CSV/Excel files
        - **Policy Evaluation**: Policy selector with predefined JSON schemas
        - **Data Operations**: Specialized interfaces for filtering and sorting
        
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