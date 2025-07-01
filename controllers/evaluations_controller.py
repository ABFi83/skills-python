from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

evaluations_bp = Blueprint('evaluations', __name__)

@evaluations_bp.route('/evaluations', methods=['GET'])
@jwt_required()
def get_all_evaluations():
    try:
        return jsonify([])  # Placeholder
    except Exception as e:
        return jsonify({'error': str(e)}), 500
