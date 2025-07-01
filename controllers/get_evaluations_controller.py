from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from extensions import db
from models.evaluation import Evaluation
from models.project import Project
from models.userproject import UserProject
from models.values import Values
from models.skill import Skill
from models.user import User
from models.role import Role
from sqlalchemy.orm import joinedload
from datetime import datetime

get_evaluations_bp = Blueprint('get_evaluations', __name__)

@get_evaluations_bp.route('/projects/<int:project_id>/evaluations', methods=['GET'])
@jwt_required()
def get_evaluations_by_project_and_date(project_id):
    # Accept both 'date' and 'evaluationDate' as query params
    evaluation_date_str = request.args.get('date') or request.args.get('evaluationDate')
    if not evaluation_date_str:
        return jsonify({'error': 'evaluationDate is required'}), 400
    try:
        # Try to parse dd/MM/yyyy
        evaluation_date = datetime.strptime(evaluation_date_str, '%d/%m/%Y').date()
    except Exception:
        try:
            # Try ISO format
            evaluation_date = datetime.fromisoformat(evaluation_date_str).date()
        except Exception:
            return jsonify({'error': 'Invalid date format'}), 400

    # Get the project with all needed relationships
    project = Project.query.options(
        joinedload(Project.user_projects).joinedload(UserProject.user),
        joinedload(Project.user_projects).joinedload(UserProject.role),
        joinedload(Project.skills),
        joinedload(Project.evaluations).joinedload(Evaluation.user),
        joinedload(Project.evaluations).joinedload(Evaluation.values).joinedload(Values.skill)
    ).filter_by(id=project_id).first()

    if not project:
        return jsonify({'error': 'Project not found'}), 404

    # Filter out users with role 'Line Manager'
    non_lm_user_projects = [up for up in project.user_projects if up.role and up.role.name != 'Line Manager']

    # Filter evaluations for the given date
    evaluations_for_date = [
        e for e in project.evaluations
        if e.evaluation_date and e.evaluation_date == evaluation_date
    ]

    if not evaluations_for_date:
        return jsonify({'error': 'No evaluations found for the specified date'}), 404

    # Build evaluation list and skill set
    evaluationLMList = []
    skill_set = set()
    for up in non_lm_user_projects:
        user_evaluations = [e for e in evaluations_for_date if e.user_id == up.user_id]
        for evaluation in user_evaluations:
            for value in evaluation.values:
                evaluationLMList.append({
                    'skillId': str(value.skill_id),
                    'score': value.value,
                    'user': {
                        'id': evaluation.user.id,
                        'username': evaluation.user.username,
                        'name': evaluation.user.name,
                        'surname': evaluation.user.surname,
                        'code': evaluation.user.code
                    }
                })
                skill_set.add(value.skill_id)

    # Get evaluated skills
    evaluated_skills = [
        {
            'id': skill.id,
            'label': skill.name,
            'shortLabel': skill.short_name
        }
        for skill in project.skills if skill.id in skill_set
    ]

    return jsonify({
        'evaluation': evaluationLMList,
        'skill': evaluated_skills
    })
