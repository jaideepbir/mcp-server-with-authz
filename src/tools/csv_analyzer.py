"""
CSV/Excel Analyzer Tool for MCP Server
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from flask import Blueprint, request, jsonify
from src.auth.auth import require_auth

csv_analyzer_bp = Blueprint('csv_analyzer', __name__)

@csv_analyzer_bp.route('/analyze', methods=['POST'])
@require_auth
def analyze_file():
    """Analyze CSV or Excel file and return statistical summary"""
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
        
        # Generate statistical summary
        summary = df.describe().to_dict()
        
        return jsonify({
            'summary': summary,
            'columns': df.columns.tolist(),
            'rows': len(df)
        }), 200
        
    except Exception as e:
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
            
        # Generate chart based on type
        if chart_type == 'bar':
            if not x_column or not y_column:
                return jsonify({'error': 'x_column and y_column required for bar chart'}), 400
            fig = px.bar(df, x=x_column, y=y_column)
        elif chart_type == 'line':
            if not x_column or not y_column:
                return jsonify({'error': 'x_column and y_column required for line chart'}), 400
            fig = px.line(df, x=x_column, y=y_column)
        elif chart_type == 'scatter':
            if not x_column or not y_column:
                return jsonify({'error': 'x_column and y_column required for scatter chart'}), 400
            fig = px.scatter(df, x=x_column, y=y_column)
        elif chart_type == 'histogram':
            if not x_column:
                return jsonify({'error': 'x_column required for histogram'}), 400
            fig = px.histogram(df, x=x_column)
        else:
            return jsonify({'error': f'Unsupported chart type: {chart_type}'}), 400
        
        # Convert to JSON
        chart_json = fig.to_json()
        
        return jsonify({
            'chart': chart_json,
            'columns': df.columns.tolist()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error visualizing data: {str(e)}'}), 500