from extensions import db
from models.project import Project
from models.userproject import UserProject
from models.project_response import ProjectResponse
from models.evaluation import Evaluation
from models.values import Values
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from datetime import datetime
import logging

log = logging.getLogger(__name__)

class ProjectService:
    def __init__(self):
        pass
    
    def calcola_media(self, values):
        """Calculate average of evaluation values"""
        if not values or len(values) == 0:
            return 0
        
        somma = sum(value.value for value in values)
        media = somma / len(values)
        return round(media, 1)
    
    def get_all_projects(self, search=None, user_id=None):
        """Retrieve all projects with optional search filter and user filter"""
        try:
            query = Project.query.options(
                joinedload(Project.client),
                joinedload(Project.skills),
                joinedload(Project.user_projects).joinedload(UserProject.user),
                joinedload(Project.user_projects).joinedload(UserProject.role),
                joinedload(Project.evaluations)
            )
            
            # Filter by user_id if provided (projects where user is involved)
            if user_id:
                query = query.join(UserProject).filter(UserProject.user_id == user_id)
            
            # Filter by search term if provided
            if search:
                query = query.filter(Project.name.like(f'{search}%'))
            
            projects = query.all()
            
            # Convert to ProjectResponse objects
            return [ProjectResponse(project) for project in projects]
            
        except Exception as e:
            print(f"Error retrieving projects: {e}")
            raise Exception("Could not retrieve projects")
    
    def get_project_detail(self, project_id, user_id):
        """Get detailed project information for a specific user"""
        try:
            project = Project.query.options(
                joinedload(Project.user_projects).joinedload(UserProject.role),
                joinedload(Project.user_projects).joinedload(UserProject.user),
                joinedload(Project.skills),
                joinedload(Project.evaluations).joinedload(Evaluation.user),
                joinedload(Project.evaluations).joinedload(Evaluation.values).joinedload(Values.skill),
                joinedload(Project.client)
            ).filter_by(id=project_id).first()
            
            print(f"DETAIL PROJECT: {project.evaluations if project else 'No project found'}")
            
            if not project:
                raise Exception("Progetto non trovato")
            
            # Filter evaluations for the specific user and sort by evaluation_date descending
            user_evaluations = [
                eval for eval in project.evaluations 
                if eval.user_id == user_id
            ]
            user_evaluations.sort(key=lambda e: e.evaluation_date, reverse=True)
            
            print(f"User evaluations found: {len(user_evaluations)}")
            log.info(f"User evaluations found: {len(user_evaluations)}")
            
            # Find user's role in this project
            user_role = None
            for up in project.user_projects:
                if up.user_id == user_id:
                    user_role = up.role
                    break
            
            # Sort skills by id descending
            project.skills.sort(key=lambda s: s.id, reverse=True)
            
            # Create response object
            response = {
                'id': project.id,
                'projectName': project.name,
                'role': {
                    'id': user_role.id if user_role else 0,
                    'code': user_role.code if user_role else "",
                    'name': user_role.name if user_role else ""
                },
                'description': project.description,
                'users': [
                    {
                        'id': up.user.id,
                        'username': up.user.username,
                        'name': up.user.name,
                        'surname': up.user.surname,
                        'code': up.user.code,
                        'role': {
                            'id': up.role.id,
                            'code': up.role.code,
                            'name': up.role.name
                        }
                    }
                    for up in project.user_projects
                ],
                'labelEvaluations': [
                    {
                        'id': skill.id,
                        'label': skill.name,
                        'shortLabel': skill.short_name
                    }
                    for skill in project.skills
                ],
                'evaluations': [],
                'client': {
                    'id': project.client.id,
                    'code': project.client.code,
                    'name': project.client.name,
                    'logo': project.client.file
                } if project.client else None
            }
            
            # Process evaluations
            for evaluation in user_evaluations:
                # Sort values by skill id descending
                evaluation.values.sort(key=lambda v: v.skill.id, reverse=True)
                
                eval_data = {
                    'id': evaluation.id,
                    'startDate': evaluation.start_date.isoformat() if evaluation.start_date else None,
                    'endDate': evaluation.end_date.isoformat() if evaluation.end_date else None,
                    'label': evaluation.evaluation_date.strftime('%d/%m/%Y') if evaluation.evaluation_date else '',
                    'ratingAverage': self.calcola_media(evaluation.values),
                    'close': evaluation.close,
                    'values': [
                        {
                            'id': value.id,
                            'skill': value.skill.name,
                            'value': value.value
                        }
                        for value in evaluation.values
                    ]
                }
                response['evaluations'].append(eval_data)
            
            return response
            
        except Exception as e:
            print(f"Error retrieving project detail: {e}")
            raise Exception("Could not retrieve project detail")
    
    def get_project_by_id(self, project_id):
        """Get project by ID"""
        try:
            return Project.query.filter_by(id=project_id).first()
        except Exception as e:
            print(f"Error retrieving project: {e}")
            raise Exception("Could not retrieve project")
    
    def create_project(self, project_data):
        """Create a new project"""
        try:
            project = Project(
                name=project_data.get('name', ''),
                description=project_data.get('description', ''),
                client_id=project_data.get('client_id')
            )
            
            db.session.add(project)
            db.session.commit()
            return project
        except Exception as e:
            db.session.rollback()
            print(f"Error creating project: {e}")
            raise Exception("Could not create project")
    
    def delete_project(self, project_id):
        """Delete project by ID"""
        try:
            print(f"Attempting to delete project with ID: {project_id}")
            project = Project.query.filter_by(id=project_id).first()
            if not project:
                print(f"Project with ID {project_id} not found")
                raise Exception("Project not found")
            
            print(f"Found project: {project.name}, proceeding with deletion")
            
            # Delete related records first to avoid foreign key constraint issues
            from models.userproject import UserProject
            from models.evaluation import Evaluation
            from models.values import Values
            
            # Delete all values related to evaluations of this project
            evaluations = Evaluation.query.filter_by(project_id=project_id).all()
            for evaluation in evaluations:
                Values.query.filter_by(evaluation_id=evaluation.id).delete()
            
            # Delete all evaluations for this project
            Evaluation.query.filter_by(project_id=project_id).delete()
            
            # Delete all user-project relationships
            UserProject.query.filter_by(project_id=project_id).delete()
            
            # Now delete the project itself
            db.session.delete(project)
            db.session.commit()
            
            print(f"Project {project_id} deleted successfully")
            return {"message": "Project deleted successfully", "id": project_id}
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting project: {str(e)}")
            print(f"Exception type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Could not delete project: {str(e)}")
    
    def get_evaluation_dates(self, project_id):
        """Get unique evaluation dates for a project, ordered by date descending"""
        try:
            # Query evaluations for the project and get distinct evaluation dates
            evaluations = db.session.query(Evaluation.evaluation_date)\
                .filter(Evaluation.project_id == project_id)\
                .filter(Evaluation.evaluation_date.isnot(None))\
                .order_by(desc(Evaluation.evaluation_date))\
                .distinct().all()
            
            # Extract dates from the query result tuples
            unique_dates = [evaluation[0] for evaluation in evaluations]
            
            log.info(f"Found {len(unique_dates)} unique evaluation dates for project {project_id}")
            return unique_dates
            
        except Exception as e:
            log.error(f"Error retrieving evaluation dates for project {project_id}: {e}")
            raise Exception("Could not retrieve evaluation dates")
    
    def update_project(self, project_id, project_data):
        """Update an existing project by ID"""
        try:
            project = Project.query.filter_by(id=project_id).first()
            if not project:
                raise Exception("Project not found")
            # Update fields from project_data
            if 'name' in project_data:
                project.name = project_data['name']
            if 'description' in project_data:
                project.description = project_data['description']
            if 'client_id' in project_data:
                project.client_id = project_data['client_id']
            # Add more fields as needed
            db.session.commit()
            return project.to_dict()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Could not update project: {e}")
    
    def create_evaluation(self, project_id, evaluation_data):
        """Create evaluations for all users in a project, one per user, for the given dates."""
        from models.evaluation import Evaluation
        from models.userproject import UserProject
        from models.project import Project
        from datetime import datetime
        try:
            project = Project.query.filter_by(id=project_id).first()
            if not project:
                raise Exception("Progetto non trovato.")
            user_projects = project.user_projects
            if not user_projects:
                raise Exception("Nessun utente associato al progetto.")
            # Parse dates from evaluation_data
            start_date = datetime.strptime(evaluation_data.get('startDate'), '%Y-%m-%d').date()
            end_date = datetime.strptime(evaluation_data.get('endDate'), '%Y-%m-%d').date()
            evaluation_date = datetime.strptime(evaluation_data.get('evaluationDate'), '%Y-%m-%d').date()
            created_evaluations = []
            for up in user_projects:
                evaluation = Evaluation(
                    user_id=up.user_id,
                    project_id=project_id,
                    start_date=start_date,
                    end_date=end_date,
                    evaluation_date=evaluation_date,
                    close=False
                )
                db.session.add(evaluation)
                created_evaluations.append(evaluation)
            db.session.commit()
            return [e.to_dict() for e in created_evaluations]
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Errore durante il salvataggio della valutazione: {e}")
    
    def save_value(self, value_data, project_id):
        """Save values for an evaluation and close it, matching Node.js saveValue logic."""
        from models.evaluation import Evaluation
        from models.values import Values
        from models.skill import Skill
        try:
            evaluation_id = value_data.get('evaluationId')
            values = value_data.get('values', [])
            
            evaluation = Evaluation.query.filter_by(id=evaluation_id, project_id=project_id).first()
            if not evaluation:
                raise Exception("Evaluation non trovato.")
            
            evaluation.close = True
            
            for v in values:
                skill_id = int(v['skill']) if isinstance(v['skill'], str) else v['skill']
                skill = Skill.query.filter_by(id=skill_id).first()
                if skill:
                    value = Values(skill_id=skill.id, evaluation_id=evaluation.id, value=v['value'])
                    db.session.add(value)
            
            db.session.commit()
            return evaluation.to_dict()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Non è stato possibile salvare i valori: {e}")
