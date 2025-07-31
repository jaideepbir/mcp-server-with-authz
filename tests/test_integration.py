"""
End-to-end integration tests for MCP Server
"""
import pytest
import requests
import time
import os

# Test configuration
BASE_URL = "http://localhost:5000"
STREAMLIT_URL = "http://localhost:8501"
OPA_URL = "http://localhost:8181"

def test_server_health():
    """Test that the MCP server is running"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_auth_login():
    """Test user authentication"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "user", "password": "user123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["username"] == "user"
    assert data["role"] == "user"

def test_csv_reader():
    """Test CSV reader functionality"""
    # First login to get token
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "user", "password": "user123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Test reading CSV file
    with open("sample_data.csv", "rb") as f:
        files = {"file": f}
        response = requests.post(
            f"{BASE_URL}/api/csv-reader/read",
            headers={"Authorization": f"Bearer {token}"},
            files=files
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "columns" in data
    assert "rows" in data

def test_opa_policies():
    """Test OPA policy listing"""
    # First login to get token
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Test listing policies
    response = requests.get(
        f"{BASE_URL}/api/opa/policies",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "policies" in data
    assert len(data["policies"]) > 0

def test_opa_evaluation():
    """Test OPA policy evaluation"""
    # First login to get token
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Test policy evaluation
    response = requests.post(
        f"{BASE_URL}/api/opa/evaluate",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "policy": "simple",
            "input": {
                "user": {"role": "admin"},
                "action": "read"
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "allowed" in data
    assert "policy" in data
    assert "input" in data

def test_streamlit_interface():
    """Test that Streamlit interface is accessible"""
    try:
        response = requests.get(STREAMLIT_URL, timeout=10)
        assert response.status_code == 200
    except requests.exceptions.RequestException:
        pytest.skip("Streamlit interface not available for testing")

def test_opa_service():
    """Test that OPA service is running"""
    try:
        response = requests.get(f"{OPA_URL}/health", timeout=10)
        assert response.status_code == 200
    except requests.exceptions.RequestException:
        pytest.skip("OPA service not available for testing")

if __name__ == "__main__":
    # Run all tests
    test_server_health()
    test_auth_login()
    test_csv_reader()
    test_opa_policies()
    test_opa_evaluation()
    test_streamlit_interface()
    test_opa_service()
    print("All integration tests passed!")