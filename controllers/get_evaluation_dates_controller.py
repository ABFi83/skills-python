from flask import Blueprint, jsonify, request
from extensions import db
from models.evaluation import Evaluation
from flask_jwt_extended import jwt_required

get_evaluation_dates_bp = Blueprint('get_evaluation_dates', __name__)

@get_evaluation_dates_bp.route('/projects/<int:project_id>/evaluations-dates', methods=['GET'])
@jwt_required()
def get_evaluation_dates(project_id):
    # Query all evaluations for the given project
    evaluations = Evaluation.query.filter_by(project_id=project_id).all()
    # Extract unique dates
    unique_dates = sorted({e.date for e in evaluations})
    return jsonify({'dates': unique_dates})
