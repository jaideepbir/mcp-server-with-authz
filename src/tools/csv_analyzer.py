"""
CSV/Excel Analyzer Tool for MCP Server
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import logging
from flask import Blueprint, request, jsonify
from src.auth.auth import require_auth

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

csv_analyzer_bp = Blueprint('csv_analyzer', __name__)

@csv_analyzer_bp.route('/analyze', methods=['POST'])
@require_auth
def analyze_file():
    """Analyze CSV or Excel file and return statistical summary"""
    try:
        # Check if file is provided in request
        if 'file' not in request.files:
            logger.warning("No file provided in request")
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            logger.warning("No file selected")
            return jsonify({'error': 'No file selected'}), 400
            
        logger.info(f"Analyzing file: {file.filename}")
        
        # Determine file type and read accordingly
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:
            logger.error(f"Unsupported file format: {file.filename}")
            return jsonify({'error': 'Unsupported file format. Please upload CSV or Excel file.'}), 400
        
        # Generate statistical summary
        summary = df.describe().to_dict()
        
        logger.info(f"Successfully analyzed {len(df)} rows")
        return jsonify({
            'summary': summary,
            'columns': df.columns.tolist(),
            'rows': len(df)
        }), 200
        
    except pd.errors.EmptyDataError:
        logger.error("Uploaded file is empty")
        return jsonify({'error': 'Uploaded file is empty'}), 400
    except pd.errors.ParserError as e:
        logger.error(f"Error parsing file: {str(e)}")
        return jsonify({'error': f'Error parsing file: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Unexpected error analyzing file: {str(e)}")
        return jsonify({'error': f'Error analyzing file: {str(e)}'}), 500

@csv_analyzer_bp.route('/visualize', methods=['POST'])
@require_auth
def visualize_data():
    """Generate Plotly visualization from CSV or Excel data"""
    try:
        # Get parameters from request
        data = request.get_json()
        chart_type = data.get('chart_type', 'bar')
        x_column = data.get('x_column')
        y_column = data.get('y_column')
        
        # Check if file is provided in request
        if 'file' not in request.files:
            logger.warning("No file provided in request")
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            logger.warning("No file selected")
            return jsonify({'error': 'No file selected'}), 400
            
        logger.info(f"Visualizing data from file: {file.filename}")
        
        # Determine file type and read accordingly
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:
            logger.error(f"Unsupported file format: {file.filename}")
            return jsonify({'error': 'Unsupported file format. Please upload CSV or Excel file.'}), 400
            
        # Validate columns
        if x_column and x_column not in df.columns:
            logger.error(f"Column '{x_column}' not found in data")
            return jsonify({'error': f"Column '{x_column}' not found in data"}), 400
            
        if y_column and y_column not in df.columns:
            logger.error(f"Column '{y_column}' not found in data")
            return jsonify({'error': f"Column '{y_column}' not found in data"}), 400
            
        # Generate chart based on type
        if chart_type == 'bar':
            if not x_column or not y_column:
                logger.error("x_column and y_column required for bar chart")
                return jsonify({'error': 'x_column and y_column required for bar chart'}), 400
            fig = px.bar(df, x=x_column, y=y_column)
        elif chart_type == 'line':
            if not x_column or not y_column:
                logger.error("x_column and y_column required for line chart")
                return jsonify({'error': 'x_column and y_column required for line chart'}), 400
            fig = px.line(df, x=x_column, y=y_column)
        elif chart_type == 'scatter':
            if not x_column or not y_column:
                logger.error("x_column and y_column required for scatter chart")
                return jsonify({'error': 'x_column and y_column required for scatter chart'}), 400
            fig = px.scatter(df, x=x_column, y=y_column)
        elif chart_type == 'histogram':
            if not x_column:
                logger.error("x_column required for histogram")
                return jsonify({'error': 'x_column required for histogram'}), 400
            fig = px.histogram(df, x=x_column)
        else:
            logger.error(f"Unsupported chart type: {chart_type}")
            return jsonify({'error': f'Unsupported chart type: {chart_type}'}), 400
        
        # Convert to JSON
        chart_json = fig.to_json()
        
        logger.info(f"Successfully generated {chart_type} chart")
        return jsonify({
            'chart': chart_json,
            'columns': df.columns.tolist()
        }), 200
        
    except pd.errors.EmptyDataError:
        logger.error("Uploaded file is empty")
        return jsonify({'error': 'Uploaded file is empty'}), 400
    except pd.errors.ParserError as e:
        logger.error(f"Error parsing file: {str(e)}")
        return jsonify({'error': f'Error parsing file: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Unexpected error visualizing data: {str(e)}")
        return jsonify({'error': f'Error visualizing data: {str(e)}'}), 500