"""
Authentication module for MCP Server
"""
import os
from functools import wraps
from flask import request, jsonify, g
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from datetime import datetime, timedelta

# In a production environment, this would be replaced with a proper user database
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

def init_auth(app):
    """Initialize JWT authentication for the app"""
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    jwt = JWTManager(app)
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """Login endpoint to generate JWT token"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Validate credentials
        if not username or not password:
            return jsonify({'message': 'Username and password required'}), 400
            
        user = USERS.get(username)
        if not user or user['password'] != password:
            return jsonify({'message': 'Invalid credentials'}), 401
            
        # Create tokens
        access_token = create_access_token(
            identity=username,
            additional_claims={"role": user['role']}
        )
        
        return jsonify({
            'access_token': access_token,
            'username': username,
            'role': user['role']
        }), 200

def require_auth(f):
    """Decorator to require authentication for specific routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verify JWT token
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Missing or invalid authorization token'}), 401
    return decorated_function

# Import verify_jwt_in_request to avoid circular import issues
from flask_jwt_extended import verify_jwt_in_request