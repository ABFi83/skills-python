from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.project_service import ProjectService

projects_bp = Blueprint('projects', __name__)
project_service = ProjectService()

@projects_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_all_projects():
    try:
        # Get user_id from JWT token
        current_user = get_jwt_identity()
        user_id = current_user.get('userId')
        
        search = request.args.get('search', '')
        project_responses = project_service.get_all_projects(search, user_id)
        return jsonify([project_response.to_dict() for project_response in project_responses])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_by_id(project_id):
    try:
        # Get user_id from JWT token for detailed view
        current_user = get_jwt_identity()
        user_id = current_user.get('userId')
        
        project_detail = project_service.get_project_detail(project_id, user_id)
        return jsonify(project_detail)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    try:
        data = request.get_json()
        project = project_service.create_project(data)
        return jsonify(project.to_dict()), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<int:project_id>/evaluations-dates', methods=['GET'])
@jwt_required()
def get_evaluation_dates(project_id):
    try:
        # Get unique evaluation dates for the project
        evaluation_dates = project_service.get_evaluation_dates(project_id)
        
        # Format dates as dd/MM/yyyy
        formatted_dates = [date.strftime('%d/%m/%Y') for date in evaluation_dates]
        
        return jsonify(formatted_dates)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project_detail(project_id):
    try:
        # Get project data from request body
        project_data = request.get_json()
        # Update the project using the service
        updated_project = project_service.update_project(project_id, project_data)
        return jsonify(updated_project)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<int:project_id>/evaluation', methods=['POST'])
@jwt_required()
def create_evaluation(project_id):
    try:
        # Get evaluation data from request body
        evaluation_data = request.get_json()
        # Create the evaluation using the service
        evaluation = project_service.create_evaluation(project_id, evaluation_data)
        return jsonify(evaluation), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<int:project_id>/values', methods=['PUT'])
@jwt_required()
def save_value(project_id):
    try:
        value_data = request.get_json()
        evaluation = project_service.save_value(value_data, project_id)
        return jsonify(evaluation)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    try:
        response = project_service.delete_project(project_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
