"""
OPA Client for MCP Server
"""
import requests
import json
import logging
import os
from flask import Blueprint, request, jsonify
from src.auth.auth import require_auth

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

opa_bp = Blueprint('opa', __name__)
OPA_URL = os.getenv("OPA_URL", "http://localhost:8181")

@opa_bp.route('/evaluate', methods=['POST'])
@require_auth
def evaluate_policy():
    """Evaluate a policy using OPA"""
    try:
        # Get policy name and input data from request
        data = request.get_json()
        if not data:
            logger.warning("No JSON data provided in request")
            return jsonify({'error': 'No JSON data provided'}), 400
            
        policy_name = data.get('policy', 'simple')
        input_data = data.get('input', {})
        
        logger.info(f"Evaluating policy: {policy_name}")
        
        # Make request to OPA
        response = requests.post(
            f"{OPA_URL}/v1/data/{policy_name}/allow",
            json={"input": input_data},
            timeout=30  # 30 second timeout
        )
        
        if response.status_code != 200:
            logger.error(f"OPA request failed with status {response.status_code}: {response.text}")
            return jsonify({'error': f'OPA request failed: {response.text}'}), 500
            
        result = response.json()
        allowed = result.get('result', False)
        
        logger.info(f"Policy evaluation result: {allowed}")
        return jsonify({
            'allowed': allowed,
            'policy': policy_name,
            'input': input_data
        }), 200
        
    except requests.exceptions.Timeout:
        logger.error("OPA request timed out")
        return jsonify({'error': 'OPA request timed out'}), 500
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to OPA service")
        return jsonify({'error': 'Could not connect to OPA service'}), 500
    except Exception as e:
        logger.error(f"Unexpected error evaluating policy: {str(e)}")
        return jsonify({'error': f'Error evaluating policy: {str(e)}'}), 500

@opa_bp.route('/policies', methods=['GET'])
@require_auth
def list_policies():
    """List available policies"""
    logger.info("Listing available policies")
    policies = ['simple', 'advanced', 'attribute_based']
    return jsonify({'policies': policies}), 200