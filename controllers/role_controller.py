from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.role_service import RoleService

role_bp = Blueprint('role', __name__)
role_service = RoleService()

@role_bp.route('/roles', methods=['GET'])
@jwt_required()
def get_all_roles():
    try:
        search = request.args.get('search', '')
        roles = role_service.get_all_roles(search)
        return jsonify([role.to_dict() for role in roles])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@role_bp.route('/roles/<int:role_id>', methods=['GET'])
@jwt_required()
def get_role_by_id(role_id):
    try:
        role = role_service.get_role_by_id(role_id)
        if not role:
            return jsonify({'message': 'Ruolo non trovato'}), 404
        return jsonify(role.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@role_bp.route('/roles', methods=['POST'])
@jwt_required()
def create_role():
    try:
        role_data = request.get_json()
        created_role = role_service.create_role(role_data)
        return jsonify(created_role.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@role_bp.route('/roles/<int:role_id>', methods=['PUT'])
@jwt_required()
def update_role(role_id):
    try:
        role_data = request.get_json()
        updated_role = role_service.update_role(role_id, role_data)
        if not updated_role:
            return jsonify({'message': 'Ruolo non trovato'}), 404
        return jsonify(updated_role.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@role_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@jwt_required()
def delete_role(role_id):
    try:
        role_service.delete_role(role_id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500
