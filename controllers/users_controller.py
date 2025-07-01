from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from services.users_service import UserService
from models.user import User
import bcrypt

users_bp = Blueprint('users', __name__)
user_service = UserService()

@users_bp.route('/users/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = user_service.get_username_password(username)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create JWT token
        access_token = create_access_token(identity={'userId': user.id, 'username': user.username})
        
        return jsonify({'token': access_token})
    
    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        search = request.args.get('search', '')
        users = user_service.get_all_users(search)
        return jsonify([user.to_dict() for user in users])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get('userId')
        
        user = user_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'message': 'Utente non trovato'}), 404
        
        return jsonify(user.to_dict())
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@users_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        user = user_service.create_user(data)
        return jsonify(user.to_dict()), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_detail(user_id):
    try:
        user = user_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'message': 'Utente non trovato'}), 404
        
        return jsonify(user.to_dict())
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500
