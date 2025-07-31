"""
CSV/Excel Reader Tool for MCP Server
"""
import pandas as pd
import logging
from flask import Blueprint, request, jsonify
from src.auth.auth import require_auth

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

csv_reader_bp = Blueprint('csv_reader', __name__)

@csv_reader_bp.route('/read', methods=['POST'])
@require_auth
def read_file():
    """Read CSV or Excel file and return data as JSON"""
    try:
        # Check if file is provided in request
        if 'file' not in request.files:
            logger.warning("No file provided in request")
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            logger.warning("No file selected")
            return jsonify({'error': 'No file selected'}), 400
            
        logger.info(f"Processing file: {file.filename}")
        
        # Determine file type and read accordingly
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:
            logger.error(f"Unsupported file format: {file.filename}")
            return jsonify({'error': 'Unsupported file format. Please upload CSV or Excel file.'}), 400
            
        # Convert to JSON
        data = df.to_dict(orient='records')
        
        logger.info(f"Successfully processed {len(data)} rows")
        return jsonify({
            'data': data,
            'columns': df.columns.tolist(),
            'rows': len(data)
        }), 200
        
    except pd.errors.EmptyDataError:
        logger.error("Uploaded file is empty")
        return jsonify({'error': 'Uploaded file is empty'}), 400
    except pd.errors.ParserError as e:
        logger.error(f"Error parsing file: {str(e)}")
        return jsonify({'error': f'Error parsing file: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Unexpected error reading file: {str(e)}")
        return jsonify({'error': f'Error reading file: {str(e)}'}), 500