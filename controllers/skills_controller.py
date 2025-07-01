from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.skill_service import SkillService

skills_bp = Blueprint('skills', __name__)
skill_service = SkillService()

@skills_bp.route('/skills', methods=['GET'])
@jwt_required()
def get_all_skills():
    try:
        search = request.args.get('search', '')
        skills = skill_service.get_all_skills(search)
        return jsonify([skill.to_dict() for skill in skills])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@skills_bp.route('/skills/<int:skill_id>', methods=['GET'])
@jwt_required()
def get_skill_by_id(skill_id):
    try:
        skill = skill_service.get_skill_by_id(skill_id)
        if not skill:
            return jsonify({'message': 'Skill non trovata'}), 404
        
        return jsonify(skill.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@skills_bp.route('/skills', methods=['POST'])
@jwt_required()
def create_skill():
    try:
        data = request.get_json()
        skill = skill_service.create_skill(data)
        return jsonify(skill.to_dict()), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
