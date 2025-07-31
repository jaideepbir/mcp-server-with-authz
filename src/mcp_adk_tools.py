#!/usr/bin/env python3
"""
MCP Tools Implementation for Google Agent Development Kit (ADK)
"""
import pandas as pd
import json
import os
from typing import Dict, Any, List, Optional

# User authentication information (simplified for demonstration)
# In a production environment, this would be replaced with a proper authentication system
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

# In-memory storage for demonstration purposes
# In a production environment, this would be replaced with a proper database or file system
DATA_STORAGE: Dict[str, pd.DataFrame] = {}

def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    """Authenticate a user and return their role
    
    Args:
        username (str): The username
        password (str): The password
        
    Returns:
        Dict[str, Any]: Authentication result with user information or error message
    """
    user = USERS.get(username)
    if user and user["password"] == password:
        return {"authenticated": True, "username": username, "role": user["role"]}
    return {"authenticated": False, "message": "Invalid credentials"}

def list_tools() -> List[str]:
    """List available tools in the MCP server
    
    Returns:
        List[str]: List of available tool names
    """
    return [
        "CSV/Excel Reader",
        "CSV/Excel Analyzer",
        "Data Filter",
        "Data Sort",
        "OPA Policy Evaluator"
    ]

def read_csv_excel(file_path: str) -> Dict[str, Any]:
    """Read a CSV or Excel file and return its contents as JSON
    
    Args:
        file_path (str): Path to the CSV or Excel file
        
    Returns:
        Dict[str, Any]: File contents with data, columns, and row count or error message
    """
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

def analyze_csv_excel(file_path: str) -> Dict[str, Any]:
    """Analyze a CSV or Excel file and return statistical summary
    
    Args:
        file_path (str): Path to the CSV or Excel file
        
    Returns:
        Dict[str, Any]: Statistical summary of the data or error message
    """
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

def filter_data(file_path: str, column: str, value: Any) -> Dict[str, Any]:
    """Filter data by column value
    
    Args:
        file_path (str): Path to the CSV or Excel file
        column (str): Column name to filter by
        value (Any): Value to filter by
        
    Returns:
        Dict[str, Any]: Filtered data or error message
    """
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

def sort_data(file_path: str, column: str, ascending: bool = True) -> Dict[str, Any]:
    """Sort data by column
    
    Args:
        file_path (str): Path to the CSV or Excel file
        column (str): Column name to sort by
        ascending (bool): Sort order (True for ascending)
        
    Returns:
        Dict[str, Any]: Sorted data or error message
    """
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

def evaluate_opa_policy(policy_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate an OPA policy with input data
    
    Args:
        policy_name (str): Name of the policy to evaluate
        input_data (Dict[str, Any]): Input data for policy evaluation
        
    Returns:
        Dict[str, Any]: Policy evaluation result with allowed status and input data
    """
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

# Export all functions
__all__ = [
    "authenticate_user",
    "list_tools",
    "read_csv_excel",
    "analyze_csv_excel",
    "filter_data",
    "sort_data",
    "evaluate_opa_policy"
]

if __name__ == "__main__":
    # For testing purposes
    print("MCP Tools for Google ADK are ready!")
    print("Available tools:", list_tools())