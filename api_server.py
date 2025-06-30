#!/usr/bin/env python3
"""
Flask API Server for Construction Project Database
Serves as a backend for the React chat interface.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from API import ConstructionProjectAPI
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the API
try:
    db_api = ConstructionProjectAPI()
    print("✅ Database API initialized successfully")
except Exception as e:
    print(f"❌ Error initializing database API: {e}")
    db_api = None

@app.route('/api/query', methods=['POST'])
def query_database():
    """Handle natural language queries from the frontend."""
    try:
        if not db_api:
            return jsonify({
                'success': False,
                'error': 'Database API not initialized',
                'natural_response': 'Sorry, the database connection is not available.'
            }), 500
        
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'No query provided',
                'natural_response': 'Please provide a query in your request.'
            }), 400
        
        natural_query = data['query'].strip()
        if not natural_query:
            return jsonify({
                'success': False,
                'error': 'Empty query',
                'natural_response': 'Please provide a non-empty query.'
            }), 400
        
        print(f"📥 Received query: {natural_query}")
        
        # Process the query using the API
        result = db_api.query_from_natural_language(natural_query)
        
        print(f"📤 Sending response: {result['success']}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Error processing query: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'natural_response': f'An error occurred while processing your query: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'database_connected': db_api is not None,
        'message': 'Construction Project API Server is running'
    })

@app.route('/api/info', methods=['GET'])
def get_database_info():
    """Get database information."""
    try:
        if not db_api:
            return jsonify({
                'error': 'Database API not initialized'
            }), 500
        
        info = db_api.get_database_info()
        return jsonify(info)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Construction Project API Server...")
    print("📊 Database API Status:", "✅ Ready" if db_api else "❌ Not Available")
    print("🌐 Server will be available at: http://localhost:5001")
    print("🔗 Health check: http://localhost:5001/api/health")
    print("ℹ️  Database info: http://localhost:5001/api/info")
    print("💬 Query endpoint: POST http://localhost:5001/api/query")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
