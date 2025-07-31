#!/usr/bin/env python3
"""
Test client for the MCP Tools compatible with Google ADK
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import our ADK-compatible MCP tools
from src.mcp_adk_tools import (
    authenticate_user,
    list_tools,
    read_csv_excel,
    analyze_csv_excel,
    filter_data,
    sort_data,
    evaluate_opa_policy
)

def main():
    """Main function to test the ADK-compatible MCP tools"""
    # Create a sample CSV file for testing
    sample_csv = """name,age,department,salary
John Doe,30,Engineering,75000
Jane Smith,25,Marketing,65000
Bob Johnson,35,Sales,70000
Alice Brown,28,Engineering,80000
Charlie Wilson,40,Management,90000"""
    
    with open("sample_data.csv", "w") as f:
        f.write(sample_csv)
    
    print("Sample CSV file created: sample_data.csv")
    
    # Test the tools
    print("\n" + "="*50)
    print("Testing ADK-compatible MCP Tools")
    print("="*50)
    
    # Test authentication
    print("\n1. Testing authentication:")
    auth_result = authenticate_user(username="user", password="user123")
    print(f"   Authentication result: {auth_result}")
    
    # List tools
    print("\n2. Listing tools:")
    tools_result = list_tools()
    print(f"   Available tools: {tools_result}")
    
    # Read CSV file
    print("\n3. Reading CSV file:")
    read_result = read_csv_excel(file_path="sample_data.csv")
    print(f"   Read result: {read_result}")
    
    # Analyze CSV file
    print("\n4. Analyzing CSV file:")
    analyze_result = analyze_csv_excel(file_path="sample_data.csv")
    print(f"   Analysis result: {analyze_result}")
    
    # Filter data
    print("\n5. Filtering data (age = 30):")
    filter_result = filter_data(
        file_path="sample_data.csv",
        column="age",
        value=30
    )
    print(f"   Filter result: {filter_result}")
    
    # Sort data
    print("\n6. Sorting data (by age, ascending):")
    sort_result = sort_data(
        file_path="sample_data.csv",
        column="age",
        ascending=True
    )
    print(f"   Sort result: {sort_result}")
    
    # Evaluate OPA policy
    print("\n7. Evaluating OPA policy:")
    policy_result = evaluate_opa_policy(
        policy_name="simple",
        input_data={"user": {"role": "user"}, "action": "read"}
    )
    print(f"   Policy evaluation result: {policy_result}")

if __name__ == "__main__":
    main()