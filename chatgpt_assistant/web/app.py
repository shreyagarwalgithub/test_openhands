import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory

from ..services.update_service import UpdateService
from ..services.research_service import ResearchService
from ..utils.storage import save_data, load_data, DATA_DIR

app = Flask(__name__)
update_service = UpdateService()
research_service = ResearchService()

@app.route('/')
def index():
    """Render the dashboard page."""
    return render_template('index.html')

@app.route('/api/update', methods=['POST'])
def generate_update():
    """Generate a new update and return the data."""
    update_data = update_service.generate_daily_update()
    
    # Save the update data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_data(f"update_{timestamp}.json", update_data)
    
    return jsonify(update_data)

@app.route('/api/updates', methods=['GET'])
def get_updates():
    """Get a list of all saved updates."""
    updates = []
    
    # List all update files in the data directory
    for filename in os.listdir(DATA_DIR):
        if filename.startswith('update_') and filename.endswith('.json'):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    updates.append({
                        'filename': filename,
                        'timestamp': data.get('timestamp', ''),
                        'num_chats': len(data.get('chats', [])),
                        'num_updates': sum(len(materials) for materials in data.get('topic_updates', {}).values())
                    })
            except Exception as e:
                print(f"Error loading update file {filename}: {str(e)}")
    
    # Sort updates by timestamp (newest first)
    updates.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return jsonify(updates)

@app.route('/api/updates/<filename>', methods=['GET'])
def get_update(filename):
    """Get a specific update by filename."""
    filepath = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'Update not found'}), 404
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': f"Error loading update: {str(e)}"}), 500

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get all tracked research topics."""
    topics = research_service.get_topics()
    return jsonify([topic.to_dict() for topic in topics])

@app.route('/api/topics', methods=['POST'])
def add_topic():
    """Add a new research topic."""
    data = request.json
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Topic name is required'}), 400
    
    topic = research_service.add_topic(
        name=data['name'],
        sources=data.get('sources', [])
    )
    
    return jsonify(topic.to_dict())

@app.route('/api/email', methods=['POST'])
def send_email():
    """Send an email with the latest update."""
    data = request.json
    
    if data and 'update_data' in data:
        update_data = data['update_data']
    else:
        # Generate a new update
        update_data = update_service.generate_daily_update()
    
    # Send the email
    success = update_service.send_email_update(update_data)
    
    if success:
        return jsonify({'status': 'success', 'message': 'Email sent successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to send email'}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files."""
    return send_from_directory('static', path)

def run_app(host='0.0.0.0', port=5000, debug=False):
    """Run the Flask application."""
    app.run(host=host, port=port, debug=debug)