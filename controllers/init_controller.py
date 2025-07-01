from flask import Blueprint, request, jsonify
from services.users_service import UserService
from services.init_service import InitService
from models.role import Role

init_bp = Blueprint('init', __name__)

@init_bp.route('/init', methods=['GET'])
def init():
    try:
        user_service = UserService()
        init_service = InitService()
        
        # Check if Team Leader role exists
        role = Role.query.filter_by(name="Team Leader").first()
        
        # Create initial users
        user1_data = {
            'name': 'zoro',
            'surname': 'zoro',
            'username': 'zoro',
            'password': 'zoro',
            'code': 'ZRO',
            'is_admin': False
        }
        
        # Check if user already exists
        existing_user = user_service.get_username_password('zoro')
        if not existing_user:
            user_service.create_user(user1_data)
        
        user2_data = {
            'name': 'sanji',
            'surname': 'sanji',
            'username': 'sanji',
            'password': 'sanji',
            'code': 'SNJ',
            'is_admin': False
        }
        
        existing_user2 = user_service.get_username_password('sanji')
        if not existing_user2:
            user_service.create_user(user2_data)
        
        user3_data = {
            'name': 'nami',
            'surname': 'nami',
            'username': 'nami',
            'password': 'nami',
            'code': 'NMI',
            'is_admin': True
        }
        
        existing_user3 = user_service.get_username_password('nami')
        if not existing_user3:
            user_service.create_user(user3_data)
        
        # Create project and return project numbers
        numbers = init_service.create_project()
        
        return jsonify(numbers), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
