from flask import Flask, request, jsonify
from .metadata_cleaner import MetadataCleaner
from .metadata_sorter import MetadataSorter
from .database_handler import DatabaseHandler

app = Flask(__name__)
cleaner = MetadataCleaner()
sorter = MetadataSorter()
db_handler = DatabaseHandler()

@app.route('/process', methods=['POST'])
def process_metadata():
    """
    Process metadata endpoint
    Expects JSON with 'metadata' field containing the metadata string
    """
    try:
        data = request.get_json()
        if not data or 'metadata' not in data:
            return jsonify({'error': 'No metadata provided'}), 400
            
        metadata_str = data['metadata']
        
        # Clean metadata
        cleaned_data = cleaner.clean_metadata(metadata_str)
        
        # Sort metadata
        sorted_data = sorter.sort_metadata(cleaned_data)
        
        # Store in database
        db_handler.store_metadata(sorted_data)
        
        return jsonify(sorted_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/retrieve', methods=['GET'])
def retrieve_metadata():
    """
    Retrieve metadata endpoint
    Optional query parameter 'category' to filter by category
    """
    try:
        category = request.args.get('category')
        data = db_handler.retrieve_metadata(category)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def start_api(host='0.0.0.0', port=5000):
    """Start the API server"""
    app.run(host=host, port=port)
