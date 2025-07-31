"""
Streamlit Web Interface for MCP Server
"""
import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

# App title and description
st.set_page_config(page_title="MCP Server", page_icon="📊", layout="wide")
st.title("📊 Multi-Component Platform (MCP) Server")
st.markdown("Welcome to the MCP Server interface. Select a tool below to get started.")

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None

# Sidebar for authentication
with st.sidebar:
    st.header("🔐 Authentication")
    auth_token = st.text_input("Enter your auth token", type="password")
    if st.button("Login"):
        if auth_token:
            # In a real application, you would authenticate with the server
            # For demo purposes, we're just storing the token
            st.session_state.token = auth_token
            st.success("Successfully logged in!")
        else:
            st.error("Please enter an auth token")

# Main content area
if not st.session_state.token:
    st.warning("Please authenticate using the sidebar to access the tools.")
else:
    # Tool selection
    st.header("🛠️ Available Tools")
    tool = st.selectbox(
        "Select a tool to use:",
        ["CSV/Excel Reader", "CSV/Excel Analyzer", "OPA Policy Evaluator"]
    )
    
    # Common headers for API requests
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }
    
    # CSV/Excel Reader tool
    if tool == "CSV/Excel Reader":
        st.subheader("📁 CSV/Excel Reader")
        st.markdown("Upload a CSV or Excel file to view its contents.")
        
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])
        
        if uploaded_file is not None:
            # Send file to API
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            try:
                response = requests.post(
                    "http://localhost:5000/api/csv-reader/read",
                    headers=headers,
                    files=files
                )
                
                if response.status_code == 200:
                    data = response.json()
                    df = pd.DataFrame(data["data"])
                    
                    # Display data
                    st.write(f"### Data Preview ({data['rows']} rows)")
                    st.dataframe(df)
                    
                    # Allow sorting and filtering
                    st.subheader("🔍 Filter and Sort Data")
                    columns = data["columns"]
                    
                    # Filter by column
                    filter_col = st.selectbox("Select column to filter", ["None"] + columns)
                    if filter_col != "None":
                        unique_values = df[filter_col].unique().tolist()
                        filter_value = st.selectbox(f"Select value for {filter_col}", unique_values)
                        filtered_df = df[df[filter_col] == filter_value]
                        st.write(f"### Filtered Data ({len(filtered_df)} rows)")
                        st.dataframe(filtered_df)
                    
                    # Sort by column
                    sort_col = st.selectbox("Select column to sort by", ["None"] + columns)
                    if sort_col != "None":
                        ascending = st.checkbox("Ascending", True)
                        sorted_df = df.sort_values(by=sort_col, ascending=ascending)
                        st.write(f"### Sorted Data ({len(sorted_df)} rows)")
                        st.dataframe(sorted_df)
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    # CSV/Excel Analyzer tool
    elif tool == "CSV/Excel Analyzer":
        st.subheader("📈 CSV/Excel Analyzer")
        st.markdown("Upload a CSV or Excel file to analyze and visualize its data.")
        
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])
        
        if uploaded_file is not None:
            # Send file to analysis API
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            try:
                response = requests.post(
                    "http://localhost:5000/api/csv-analyzer/analyze",
                    headers=headers,
                    files=files
                )
                
                if response.status_code == 0:
                    data = response.json()
                    st.write("### Statistical Summary")
                    st.json(data["summary"])
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error analyzing file: {str(e)}")
            
            # Visualization options
            st.subheader("📊 Data Visualization")
            chart_type = st.selectbox("Select chart type", ["bar", "line", "scatter", "histogram"])
            
            # Get column names for chart
            try:
                # Read file again to get columns
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                columns = df.columns.tolist()
                
                x_column = None
                y_column = None
                
                if chart_type != "histogram":
                    x_column = st.selectbox("Select X-axis column", columns)
                    y_column = st.selectbox("Select Y-axis column", columns)
                else:
                    x_column = st.selectbox("Select column for histogram", columns)
                
                # Prepare data for visualization API
                viz_data = {
                    "chart_type": chart_type,
                    "x_column": x_column
                }
                
                if chart_type != "histogram":
                    viz_data["y_column"] = y_column
                
                # Send to visualization API
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(
                    "http://localhost:5000/api/csv-analyzer/visualize",
                    headers=headers,
                    files=files,
                    data={"chart_type": chart_type, "x_column": x_column, "y_column": y_column if y_column else ""}
                )
                
                if response.status_code == 200:
                    chart_data = response.json()
                    # Display chart
                    st.write("### Chart")
                    fig = go.Figure(json.loads(chart_data["chart"]))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error visualizing data: {str(e)}")
    
    # OPA Policy Evaluator tool
    elif tool == "OPA Policy Evaluator":
        st.subheader("🛡️ OPA Policy Evaluator")
        st.markdown("Evaluate access control policies using Open Policy Agent.")
        
        # Get available policies
        try:
            response = requests.get(
                "http://localhost:5000/api/opa/policies",
                headers=headers
            )
            
            if response.status_code == 200:
                policies = response.json()["policies"]
                selected_policy = st.selectbox("Select policy", policies)
                
                # Input data for policy evaluation
                st.subheader("📝 Policy Input")
                user_role = st.selectbox("User Role", ["admin", "user"])
                action = st.selectbox("Action", ["read", "write"])
                
                # Policy-specific inputs
                if selected_policy == "advanced":
                    user_department = st.text_input("User Department")
                    doc_department = st.text_input("Document Department")
                    input_data = {
                        "user": {
                            "role": user_role,
                            "department": user_department
                        },
                        "action": action,
                        "document": {
                            "department": doc_department
                        }
                    }
                elif selected_policy == "attribute_based":
                    clearance_level = st.number_input("User Clearance Level", min_value=0, max_value=10, value=1)
                    classification_level = st.number_input("Document Classification Level", min_value=0, max_value=10, value=1)
                    user_groups = st.text_input("User Groups (comma-separated)")
                    doc_group = st.text_input("Document Group")
                    input_data = {
                        "user": {
                            "role": user_role,
                            "clearance_level": clearance_level,
                            "groups": [g.strip() for g in user_groups.split(",") if g.strip()]
                        },
                        "action": action,
                        "document": {
                            "classification_level": classification_level,
                            "group": doc_group
                        }
                    }
                else:  # simple policy
                    input_data = {
                        "user": {
                            "role": user_role
                        },
                        "action": action
                    }
                
                # Evaluate policy
                if st.button("Evaluate Policy"):
                    eval_data = {
                        "policy": selected_policy,
                        "input": input_data
                    }
                    
                    response = requests.post(
                        "http://localhost:5000/api/opa/evaluate",
                        headers=headers,
                        json=eval_data
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result["allowed"]:
                            st.success("✅ Access Granted")
                        else:
                            st.error("❌ Access Denied")
                        
                        st.json(result)
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            else:
                st.error(f"Error fetching policies: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error connecting to policy service: {str(e)}")