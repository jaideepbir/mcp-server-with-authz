#!/usr/bin/env python3
"""
MCP Server Implementation for CSV/Excel Processing and OPA Policy Evaluation
"""
import pandas as pd
import json
import os
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from mcp.types import TextResourceContents

# Create an MCP server, binding to all interfaces
mcp = FastMCP("MCP Data Processing Server", host="0.0.0.0", port=8000)

# In-memory storage for demonstration purposes
# In a production environment, this would be replaced with a proper database or file system
DATA_STORAGE: Dict[str, pd.DataFrame] = {}

# User authentication information (simplified for demonstration)
# In a production environment, this would be replaced with a proper authentication system
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

@mcp.tool()
def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    """Authenticate a user and return their role"""
    user = USERS.get(username)
    if user and user["password"] == password:
        return {"authenticated": True, "username": username, "role": user["role"]}
    return {"authenticated": False, "message": "Invalid credentials"}

@mcp.tool()
def list_tools() -> List[str]:
    """List available tools in the MCP server"""
    return [
        "CSV/Excel Reader",
        "CSV/Excel Analyzer",
        "Data Filter",
        "Data Sort",
        "OPA Policy Evaluator"
    ]

@mcp.tool()
def read_csv_excel(file_path: str) -> Dict[str, Any]:
    """Read a CSV or Excel file and return its contents as JSON"""
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            return {"error": "Unsupported file format. Please provide a CSV or Excel file."}
        
        # Store in memory for later use
        DATA_STORAGE[file_path] = df
        
        return {
            "data": df.to_dict(orient='records'),
            "columns": df.columns.tolist(),
            "rows": len(df)
        }
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}

@mcp.tool()
def analyze_csv_excel(file_path: str) -> Dict[str, Any]:
    """Analyze a CSV or Excel file and return statistical summary"""
    try:
        # Check if file is already loaded
        if file_path in DATA_STORAGE:
            df = DATA_STORAGE[file_path]
        else:
            # Load file if not already in memory
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                return {"error": "Unsupported file format. Please provide a CSV or Excel file."}
            
            # Store in memory for later use
            DATA_STORAGE[file_path] = df
        
        # Generate statistical summary
        summary = df.describe().to_dict()
        
        return {
            "summary": summary,
            "columns": df.columns.tolist(),
            "rows": len(df)
        }
    except Exception as e:
        return {"error": f"Error analyzing file: {str(e)}"}

@mcp.tool()
def filter_data(file_path: str, column: str, value: Any) -> Dict[str, Any]:
    """Filter data by column value"""
    try:
        # Check if file is already loaded
        if file_path in DATA_STORAGE:
            df = DATA_STORAGE[file_path]
        else:
            return {"error": "File not loaded. Please read the file first."}
        
        # Filter data
        filtered_df = df[df[column] == value]
        
        return {
            "data": filtered_df.to_dict(orient='records'),
            "columns": filtered_df.columns.tolist(),
            "rows": len(filtered_df)
        }
    except Exception as e:
        return {"error": f"Error filtering data: {str(e)}"}

@mcp.tool()
def sort_data(file_path: str, column: str, ascending: bool = True) -> Dict[str, Any]:
    """Sort data by column"""
    try:
        # Check if file is already loaded
        if file_path in DATA_STORAGE:
            df = DATA_STORAGE[file_path]
        else:
            return {"error": "File not loaded. Please read the file first."}
        
        # Sort data
        sorted_df = df.sort_values(by=column, ascending=ascending)
        
        return {
            "data": sorted_df.to_dict(orient='records'),
            "columns": sorted_df.columns.tolist(),
            "rows": len(sorted_df)
        }
    except Exception as e:
        return {"error": f"Error sorting data: {str(e)}"}

@mcp.tool()
def evaluate_opa_policy(policy_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate an OPA policy with input data"""
    # This is a simplified implementation
    # In a real implementation, this would call the OPA service
    
    # Simple policy evaluation logic
    if policy_name == "simple":
        # Allow admins to do anything, users to read only
        user_role = input_data.get("user", {}).get("role", "")
        action = input_data.get("action", "")
        
        if user_role == "admin":
            allowed = True
        elif user_role == "user" and action == "read":
            allowed = True
        else:
            allowed = False
            
    elif policy_name == "advanced":
        # Users can access documents in their department
        user_role = input_data.get("user", {}).get("role", "")
        user_department = input_data.get("user", {}).get("department", "")
        doc_department = input_data.get("document", {}).get("department", "")
        action = input_data.get("action", "")
        
        if user_role == "admin":
            allowed = True
        elif user_role == "user" and action == "read":
            allowed = True
        elif user_role == "user" and action == "write" and user_department == doc_department:
            allowed = True
        else:
            allowed = False
            
    elif policy_name == "attribute_based":
        # Users can access documents based on clearance level
        user_role = input_data.get("user", {}).get("role", "")
        user_clearance = input_data.get("user", {}).get("clearance_level", 0)
        doc_classification = input_data.get("document", {}).get("classification_level", 0)
        
        if user_role == "admin":
            allowed = True
        elif user_role == "user" and user_clearance >= doc_classification:
            allowed = True
        else:
            allowed = False
    else:
        allowed = False
    
    return {
        "allowed": allowed,
        "policy": policy_name,
        "input": input_data
    }

@mcp.resource("file://{file_path}")
def get_file_content(file_path: str) -> TextResourceContents:
    """Get the content of a file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return TextResourceContents(text=content, uri=f"file://{file_path}")
    except Exception as e:
        return TextResourceContents(text=f"Error reading file: {str(e)}", uri=f"file://{file_path}")

@mcp.prompt()
def csv_analysis_prompt(file_path: str) -> str:
    """Generate a prompt for CSV analysis"""
    return f"""
    Please analyze the CSV file at {file_path} and provide:
    1. Summary statistics for numerical columns
    2. Information about categorical columns
    3. Any interesting patterns or outliers you notice
    4. Suggestions for data visualization
    """

@mcp.prompt()
def opa_policy_evaluation_prompt(policy_name: str, user_role: str, action: str) -> str:
    """Generate a prompt for OPA policy evaluation"""
    return f"""
    Please evaluate the {policy_name} policy for a {user_role} user performing a {action} action.
    Consider:
    1. The policy rules and constraints
    2. Whether the action should be allowed or denied
    3. Any edge cases or special considerations
    4. Suggestions for policy improvement
    """

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport='sse')