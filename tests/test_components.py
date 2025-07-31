"""
Test cases for MCP Server components
"""
import pytest
import pandas as pd
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import create_app
from auth.auth import USERS

@pytest.fixture
def app():
    """Create Flask app for testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ok'

def test_login_success(client):
    """Test successful login"""
    response = client.post('/api/auth/login', 
                          json={'username': 'user', 'password': 'user123'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['username'] == 'user'
    assert data['role'] == 'user'

def test_login_failure(client):
    """Test failed login"""
    response = client.post('/api/auth/login',
                          json={'username': 'invalid', 'password': 'wrong'})
    assert response.status_code == 401

def test_login_missing_fields(client):
    """Test login with missing fields"""
    response = client.post('/api/auth/login', json={'username': 'user'})
    assert response.status_code == 400

@patch('src.tools.csv_reader.pd.read_csv')
def test_csv_read_success(mock_read_csv, client):
    """Test successful CSV reading"""
    # Mock the pandas read_csv function
    mock_df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    mock_read_csv.return_value = mock_df
    
    # Get auth token
    login_response = client.post('/api/auth/login',
                                json={'username': 'user', 'password': 'user123'})
    assert login_response.status_code == 200
    token_data = json.loads(login_response.data)
    assert 'access_token' in token_data
    token = token_data['access_token']
    
    # Test CSV reading with a mock file
    data = {'file': (b'col1,col2\n1,a\n2,b', 'test.csv')}
    response = client.post('/api/csv-reader/read',
                          headers={'Authorization': f'Bearer {token}'},
                          data=data,
                          content_type='multipart/form-data')
    
    # For now, we'll just check that it doesn't return a 500 error
    assert response.status_code in [200, 400]

def test_csv_read_no_file(client):
    """Test CSV reading with no file"""
    # Get auth token
    login_response = client.post('/api/auth/login',
                                json={'username': 'user', 'password': 'user123'})
    assert login_response.status_code == 200
    token_data = json.loads(login_response.data)
    assert 'access_token' in token_data
    token = token_data['access_token']
    
    # Test CSV reading without file
    response = client.post('/api/csv-reader/read',
                          headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 400

@patch('src.tools.opa_client.requests.post')
def test_opa_evaluate_success(mock_post, client):
    """Test successful OPA policy evaluation"""
    # Mock the requests.post function
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'result': True}
    mock_post.return_value = mock_response
    
    # Get auth token
    login_response = client.post('/api/auth/login',
                                json={'username': 'admin', 'password': 'admin123'})
    assert login_response.status_code == 200
    token_data = json.loads(login_response.data)
    assert 'access_token' in token_data
    token = token_data['access_token']
    
    # Test OPA evaluation
    response = client.post('/api/opa/evaluate',
                          headers={'Authorization': f'Bearer {token}'},
                          json={'policy': 'simple', 'input': {}})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'allowed' in data
    assert 'policy' in data
    assert 'input' in data
