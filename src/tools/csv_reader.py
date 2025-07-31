"""
CSV/Excel Reader Tool for MCP Server
"""
import pandas as pd
from flask import Blueprint, request, jsonify
from src.auth.auth import require_auth

csv_reader_bp = Blueprint('csv_reader', __name__)

@csv_reader_bp.route('/read', methods=['POST'])
@require_auth
def read_file():
    """Read CSV or Excel file and return data as JSON"""
    try:
        # Check if file is provided in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        # Determine file type and read accordingly
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:
            return jsonify({'error': 'Unsupported file format. Please upload CSV or Excel file.'}), 400
            
        # Convert to JSON
        data = df.to_dict(orient='records')
        return jsonify({
            'data': data,
            'columns': df.columns.tolist(),
            'rows': len(data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error reading file: {str(e)}'}), 500