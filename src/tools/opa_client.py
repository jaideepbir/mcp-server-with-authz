"""
OPA Client for MCP Server
"""
import requests
import json
from flask import Blueprint, request, jsonify
from src.auth.auth import require_auth

opa_bp = Blueprint('opa', __name__)
OPA_URL = "http://localhost:8181"

@opa_bp.route('/evaluate', methods=['POST'])
@require_auth
def evaluate_policy():
    """Evaluate a policy using OPA"""
    try:
        # Get policy name and input data from request
        data = request.get_json()
        policy_name = data.get('policy', 'simple')
        input_data = data.get('input', {})
        
        # Make request to OPA
        response = requests.post(
            f"{OPA_URL}/v1/data/{policy_name}/allow",
            json={"input": input_data}
        )
        
        if response.status_code != 200:
            return jsonify({'error': f'OPA request failed: {response.text}'}), 500
            
        result = response.json()
        allowed = result.get('result', False)
        
        return jsonify({
            'allowed': allowed,
            'policy': policy_name,
            'input': input_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error evaluating policy: {str(e)}'}), 500

@opa_bp.route('/policies', methods=['GET'])
@require_auth
def list_policies():
    """List available policies"""
    policies = ['simple', 'advanced', 'attribute_based']
    return jsonify({'policies': policies}), 200