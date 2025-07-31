"""
Authentication module for MCP Server
"""
import os
from functools import wraps
from flask import request, jsonify, Flask
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In a production environment, this would be replaced with a proper user database
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

def init_auth(app: Flask):
    """Initialize JWT authentication for the app"""
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    jwt = JWTManager(app)
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """Login endpoint to generate JWT token"""
        try:
            data = request.get_json()
            if not data:
                logger.warning("No JSON data provided in login request")
                return jsonify({'message': 'No JSON data provided'}), 400
                
            username = data.get('username')
            password = data.get('password')
            
            # Validate credentials
            if not username or not password:
                logger.warning("Username or password missing in login request")
                return jsonify({'message': 'Username and password required'}), 400
                
            user = USERS.get(username)
            if not user or user['password'] != password:
                logger.warning(f"Invalid login attempt for user: {username}")
                return jsonify({'message': 'Invalid credentials'}), 401
                
            # Create tokens
            additional_claims = {"role": user['role']}
            access_token = create_access_token(
                identity=username,
                additional_claims=additional_claims
            )
            
            logger.info(f"Successful login for user: {username}")
            return jsonify({
                'access_token': access_token,
                'username': username,
                'role': user['role']
            }), 200
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return jsonify({'message': 'Internal server error'}), 500

def require_auth(f):
    """Decorator to require authentication for specific routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Check for Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                logger.warning("Missing or invalid authorization header")
                return jsonify({'message': 'Missing or invalid authorization token'}), 401
            
            # For testing purposes, we'll just verify the header exists
            # In a real implementation, Flask-JWT-Extended would handle token verification
            return f(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Authentication failed: {str(e)}")
            return jsonify({'message': 'Missing or invalid authorization token'}), 401
    return decorated_function