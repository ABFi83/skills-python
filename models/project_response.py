class ProjectResponse:
    def __init__(self, project):
        self.id = project.id
        self.projectName = project.name
        self.description = project.description
        
        # Evaluations information
        self.evaluations = []
        if project.evaluations:
            self.evaluations = [
                {
                    'id': evaluation.id,
                    'user_id': evaluation.user_id,
                    'project_id': evaluation.project_id,
                    'start_date': evaluation.start_date.isoformat() if evaluation.start_date else None,
                    'end_date': evaluation.end_date.isoformat() if evaluation.end_date else None,
                    'close': evaluation.close,
                    'evaluation_date': evaluation.evaluation_date.isoformat() if evaluation.evaluation_date else None
                }
                for evaluation in project.evaluations
            ]
        
        # Label evaluations (placeholder for now)
        self.labelEvaluations = []
        
        # Role information (from user projects - taking the first role if any)
        self.role = None
        if project.user_projects and len(project.user_projects) > 0:
            first_role = project.user_projects[0].role
            if first_role:
                self.role = {
                    'id': first_role.id,
                    'name': first_role.name,
                    'code': first_role.code
                }
        
        # Users information (from user projects)
        self.users = []
        if project.user_projects:
            self.users = [
                {
                    'id': up.user.id,
                    'name': up.user.name,
                    'surname': up.user.surname,
                    'username': up.user.username,
                    'code': up.user.code,
                    'is_admin': up.user.is_admin
                }
                for up in project.user_projects if up.user
            ]
        
        # Client information
        self.client = None
        if project.client:
            self.client = {
                'id': project.client.id,
                'name': project.client.name,
                'code': project.client.code,
                'file': project.client.file
            }
    
    def to_dict(self):
        return {
            'id': self.id,
            'projectName': self.projectName,
            'description': self.description,
            'evaluations': self.evaluations,
            'labelEvaluations': self.labelEvaluations,
            'role': self.role,
            'users': self.users,
            'client': self.client
        }
