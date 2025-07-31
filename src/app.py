"""
Main application file for MCP Server
"""
import os
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields
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
    
    # Initialize API documentation
    api = Api(
        app,
        version='1.0',
        title='MCP Server API',
        description='Multi-Component Platform Server API Documentation',
        doc='/docs/',
        prefix='/api'
    )
    
    # Define API models for documentation
    login_model = api.model('Login', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password')
    })
    
    token_model = api.model('Token', {
        'access_token': fields.String(description='JWT Access Token'),
        'username': fields.String(description='Username'),
        'role': fields.String(description='User Role')
    })
    
    error_model = api.model('Error', {
        'message': fields.String(description='Error message')
    })
    
    csv_data_model = api.model('CSVData', {
        'data': fields.List(fields.Raw, description='Data rows'),
        'columns': fields.List(fields.String, description='Column names'),
        'rows': fields.Integer(description='Number of rows')
    })
    
    policy_list_model = api.model('PolicyList', {
        'policies': fields.List(fields.String, description='Available policies')
    })
    
    policy_input_model = api.model('PolicyInput', {
        'policy': fields.String(description='Policy name'),
        'input': fields.Raw(description='Input data for policy evaluation')
    })
    
    policy_result_model = api.model('PolicyResult', {
        'allowed': fields.Boolean(description='Whether access is allowed'),
        'policy': fields.String(description='Policy name'),
        'input': fields.Raw(description='Input data for policy evaluation')
    })
    
    # Add documentation for auth endpoints
    ns_auth = api.namespace('auth', description='Authentication operations')
    
    @ns_auth.route('/login')
    class Login(Resource):
        @ns_auth.expect(login_model)
        @ns_auth.marshal_with(token_model, code=200)
        @ns_auth.response(400, 'Missing fields', error_model)
        @ns_auth.response(401, 'Invalid credentials', error_model)
        def post(self):
            """Generate JWT token"""
            pass  # Implementation in auth module
    
    # Add documentation for CSV reader endpoints
    ns_csv_reader = api.namespace('csv-reader', description='CSV/Excel reader operations')
    
    @ns_csv_reader.route('/read')
    class CSVReader(Resource):
        @ns_csv_reader.doc('read_csv')
        @ns_csv_reader.produces(['multipart/form-data'])
        @ns_csv_reader.response(200, 'Success', csv_data_model)
        @ns_csv_reader.response(400, 'Bad Request', error_model)
        @ns_csv_reader.response(401, 'Unauthorized', error_model)
        @ns_csv_reader.response(500, 'Internal Server Error', error_model)
        def post(self):
            """Read CSV or Excel file"""
            pass  # Implementation in csv_reader module
    
    # Add documentation for CSV analyzer endpoints
    ns_csv_analyzer = api.namespace('csv-analyzer', description='CSV/Excel analyzer operations')
    
    @ns_csv_analyzer.route('/analyze')
    class CSVAnalyzer(Resource):
        @ns_csv_analyzer.doc('analyze_csv')
        @ns_csv_analyzer.produces(['multipart/form-data'])
        @ns_csv_analyzer.response(200, 'Success', csv_data_model)
        @ns_csv_analyzer.response(400, 'Bad Request', error_model)
        @ns_csv_analyzer.response(401, 'Unauthorized', error_model)
        @ns_csv_analyzer.response(500, 'Internal Server Error', error_model)
        def post(self):
            """Analyze CSV or Excel file"""
            pass  # Implementation in csv_analyzer module
    
    @ns_csv_analyzer.route('/visualize')
    class CSVVisualizer(Resource):
        @ns_csv_analyzer.doc('visualize_csv')
        @ns_csv_analyzer.produces(['multipart/form-data'])
        @ns_csv_analyzer.response(200, 'Success')
        @ns_csv_analyzer.response(400, 'Bad Request', error_model)
        @ns_csv_analyzer.response(401, 'Unauthorized', error_model)
        @ns_csv_analyzer.response(500, 'Internal Server Error', error_model)
        def post(self):
            """Generate visualization from CSV or Excel data"""
            pass  # Implementation in csv_analyzer module
    
    # Add documentation for OPA endpoints
    ns_opa = api.namespace('opa', description='OPA client operations')
    
    @ns_opa.route('/policies')
    class OPAPolicies(Resource):
        @ns_opa.doc('list_policies')
        @ns_opa.marshal_with(policy_list_model, code=200)
        @ns_opa.response(401, 'Unauthorized', error_model)
        def get(self):
            """List available policies"""
            pass  # Implementation in opa_client module
    
    @ns_opa.route('/evaluate')
    class OPAEvaluate(Resource):
        @ns_opa.doc('evaluate_policy')
        @ns_opa.expect(policy_input_model)
        @ns_opa.marshal_with(policy_result_model, code=200)
        @ns_opa.response(400, 'Bad Request', error_model)
        @ns_opa.response(401, 'Unauthorized', error_model)
        @ns_opa.response(500, 'Internal Server Error', error_model)
        def post(self):
            """Evaluate policy with input data"""
            pass  # Implementation in opa_client module
    
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