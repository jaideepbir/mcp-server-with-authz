"""
Authentication module for MCP Server
"""
import os
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

def init_auth(app):
    """Initialize JWT authentication for the app"""
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    jwt = JWTManager(app)
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """Login endpoint to generate JWT token"""
        # In a real application, you would verify credentials here
        # For demo purposes, we're just checking if a token is provided
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Missing or invalid authorization token'}), 401
            
        # Create a token for the user
        access_token = create_access_token(identity='user')
        return jsonify(access_token=access_token), 200

def require_auth(f):
    """Decorator to require authentication for specific routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Missing or invalid authorization token'}), 401
        return f(*args, **kwargs)
    return decorated_function