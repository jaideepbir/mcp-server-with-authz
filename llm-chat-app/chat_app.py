#!/usr/bin/env python3
"""
LLM Chat Application with MCP Integration

This application provides a chat interface that connects to an LLM and integrates with an MCP server,
allowing the LLM to access tools and resources for enhanced functionality.
"""

import streamlit as st
import openai
from mcp import Client
from mcp.client.sse import sse_client
import json
import asyncio

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'mcp_client' not in st.session_state:
    st.session_state.mcp_client = None
if 'mcp_connected' not in st.session_state:
    st.session_state.mcp_connected = False

def initialize_session_state():
    """Initialize session state variables"""
    if 'mcp_server_url' not in st.session_state:
        st.session_state.mcp_server_url = "http://localhost:8000/sse"
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'model_choice' not in st.session_state:
        st.session_state.model_choice = "gpt-3.5-turbo"
    if 'tool_results' not in st.session_state:
        st.session_state.tool_results = []

# Set page config
st.set_page_config(
    page_title="LLM Chat with MCP",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 LLM Chat with MCP Integration")
st.caption("Chat with an LLM that can access tools and resources through the Model Context Protocol")

# Initialize session state
initialize_session_state()

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # API key input
    api_key = st.text_input(
        "OpenAI API Key",
        value=st.session_state.api_key,
        type="password",
        help="Your OpenAI API key for accessing LLMs"
    )
    st.session_state.api_key = api_key
    
    # Model selection
    model_choice = st.selectbox(
        "Model",
        options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0,
        help="Select the LLM to use for chatting"
    )
    st.session_state.model_choice = model_choice
    
    # MCP server URL input
    mcp_server_url = st.text_input(
        "MCP Server URL",
        value=st.session_state.mcp_server_url,
        help="URL of your MCP server (usually ends with /sse)"
    )
    st.session_state.mcp_server_url = mcp_server_url
    
    # MCP connection status
    if st.session_state.mcp_connected:
        st.success("Connected to MCP server")
    else:
        st.warning("Not connected to MCP server")
    
    # MCP connection buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Connect to MCP", disabled=st.session_state.mcp_connected or not mcp_server_url):
            try:
                # In a real implementation, we would connect to the MCP server here
                st.session_state.mcp_connected = True
                st.session_state.mcp_client = "mock_client"  # Placeholder
                st.rerun()
            except Exception as e:
                st.error(f"Failed to connect to MCP server: {str(e)}")
    
    with col2:
        if st.button("Disconnect", disabled=not st.session_state.mcp_connected):
            st.session_state.mcp_connected = False
            st.session_state.mcp_client = None
            st.rerun()
    
    # Reset conversation
    if st.button("Reset Conversation"):
        st.session_state.conversation = []
        st.session_state.tool_results = []
        st.rerun()

# Main chat interface
chat_col, tools_col = st.columns([2, 1])

with chat_col:
    st.subheader("Conversation")
    
    # Display conversation history
    for message in st.session_state.conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "tool_calls" in message:
                with st.expander("Tool Calls"):
                    st.json(message["tool_calls"])
    
    # User input
    if prompt := st.chat_input("Message the LLM..."):
        # Add user message to conversation
        st.session_state.conversation.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate LLM response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Configure OpenAI client
                if not api_key:
                    st.error("Please enter your OpenAI API key in the sidebar")
                    st.stop()
                
                client = openai.OpenAI(api_key=api_key)
                
                # Prepare messages for LLM
                messages = []
                for msg in st.session_state.conversation:
                    # Skip tool call messages that are internal implementation details
                    if not msg.get("tool_call"):
                        messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                
                # Add context about available tools if connected to MCP
                if st.session_state.mcp_connected:
                    messages.append({
                        "role": "system",
                        "content": "You have access to tools through the MCP (Model Context Protocol). "
                                  "You can use these tools to access data, perform analysis, and more. "
                                  "To use a tool, respond with a JSON object describing the tool call."
                    })
                
                # Generate response from LLM
                response = client.chat.completions.create(
                    model=st.session_state.model_choice,
                    messages=messages,
                    stream=True,
                )
                
                # Stream response
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                # Add assistant response to conversation
                st.session_state.conversation.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tools_col:
    st.subheader("MCP Tools")
    
    if st.session_state.mcp_connected:
        # In a real implementation, we would fetch available tools from the MCP server
        # For now, we'll show mock tools based on our server capabilities
        mock_tools = [
            {
                "name": "authenticate_user",
                "description": "Authenticate a user with username and password",
                "parameters": {
                    "username": "string",
                    "password": "string"
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
                    "file_path": "string"
                }
            },
            {
                "name": "analyze_csv_excel",
                "description": "Analyze a CSV or Excel file and return statistical summary",
                "parameters": {
                    "file_path": "string"
                }
            },
            {
                "name": "filter_data",
                "description": "Filter data by column value",
                "parameters": {
                    "file_path": "string",
                    "column": "string",
                    "value": "any"
                }
            },
            {
                "name": "sort_data",
                "description": "Sort data by column",
                "parameters": {
                    "file_path": "string",
                    "column": "string",
                    "ascending": "boolean"
                }
            },
            {
                "name": "evaluate_opa_policy",
                "description": "Evaluate an OPA policy with input data",
                "parameters": {
                    "policy_name": "string",
                    "input_data": "object"
                }
            }
        ]
        
        # Display tools
        st.markdown("### Available Tools")
        for tool in mock_tools:
            with st.expander(tool["name"]):
                st.markdown(f"**Description:** {tool['description']}")
                if tool["parameters"]:
                    st.markdown("**Parameters:**")
                    for param, param_type in tool["parameters"].items():
                        st.code(f"{param}: {param_type}")
                else:
                    st.markdown("_No parameters required_")
        
        # Tool execution section
        st.markdown("### Execute Tool")
        selected_tool = st.selectbox(
            "Select Tool",
            [tool["name"] for tool in mock_tools],
            key="selected_tool"
        )
        
        # Get selected tool details
        tool_details = next((tool for tool in mock_tools if tool["name"] == selected_tool), None)
        if tool_details:
            st.markdown(f"**Tool:** {tool_details['name']}")
            st.markdown(f"**Description:** {tool_details['description']}")
            
            # Parameter inputs
            tool_params = {}
            if tool_details["parameters"]:
                st.markdown("**Parameters:**")
                for param, param_type in tool_details["parameters"].items():
                    if param_type == "string":
                        tool_params[param] = st.text_input(param)
                    elif param_type == "boolean":
                        tool_params[param] = st.checkbox(param)
                    elif param_type == "number":
                        tool_params[param] = st.number_input(param)
                    else:  # object and other types
                        tool_params[param] = st.text_area(param, height=100)
                        # Try to parse as JSON
                        if tool_params[param].strip():
                            try:
                                tool_params[param] = json.loads(tool_params[param])
                            except:
                                pass
            
            # Execute button
            if st.button("Execute Tool"):
                # In a real implementation, we would execute the tool through the MCP client
                # For now, we'll simulate the result
                st.session_state.tool_results.append({
                    "tool": selected_tool,
                    "parameters": tool_params,
                    "timestamp": "2025-08-01T12:00:00Z",
                    "result": f"Simulated result for {selected_tool} with parameters: {json.dumps(tool_params, indent=2)}"
                })
                st.rerun()
    
    else:
        st.info("Connect to an MCP server to see available tools")
    
    # Display tool execution results
    if st.session_state.tool_results:
        st.markdown("### Tool Results")
        for i, result in enumerate(st.session_state.tool_results):
            with st.expander(f"Result {i+1}: {result['tool']}"):
                st.json(result)

# Footer
st.markdown("---")
st.caption("LLM Chat with MCP Integration")