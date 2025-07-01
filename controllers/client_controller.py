from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required
import os

client_bp = Blueprint('client', __name__)

@client_bp.route('/clients', methods=['GET'])
@jwt_required()
def get_all_clients():
    try:
        return jsonify([])  # Placeholder
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@client_bp.route('/logo/<client_id>', methods=['GET'])
def get_client_logo(client_id):
    try:
        # Get dynamic path to images directory
        # Go up from controllers to skills-python directory, then to images
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  # Go up 1 level from controllers to skills-python
        images_dir = os.path.join(project_root, 'images')
        
        # Image filename
        image_filename = f"{client_id}.jpg"
        
        print(f"Image path: {os.path.join(images_dir, image_filename)}")
        
        # Check if file exists
        image_path = os.path.join(images_dir, image_filename)
        if not os.path.exists(image_path):
            return jsonify({'error': 'Logo non trovato'}), 404
        
        # Send the file
        return send_from_directory(images_dir, image_filename)
        
    except Exception as e:
        print(f"Error serving logo: {e}")
        return jsonify({'error': 'Logo non trovato'}), 404
