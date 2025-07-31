"""
Main application file for MCP Server
"""
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from src.auth.auth import init_auth
from src.tools.csv_reader import csv_reader_bp
from src.tools.csv_analyzer import csv_analyzer_bp
from src.tools.opa_client import opa_bp

load_dotenv()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Initialize CORS
    CORS(app)
    
    # Initialize authentication
    init_auth(app)
    
    # Register blueprints
    app.register_blueprint(csv_reader_bp, url_prefix='/api/csv-reader')
    app.register_blueprint(csv_analyzer_bp, url_prefix='/api/csv-analyzer')
    app.register_blueprint(opa_bp, url_prefix='/api/opa')
    
    @app.route('/')
    def health_check():
        return {'status': 'ok', 'message': 'MCP Server is running'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )