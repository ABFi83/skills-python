from extensions import db
from sqlalchemy.orm import relationship

class UserProject(db.Model):
    __tablename__ = 'user_project'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="user_projects")
    project = relationship("Project", back_populates="user_projects")
    role = relationship("Role", back_populates="user_projects")
    
    def __init__(self, user_id, project_id, role_id):
        self.user_id = user_id
        self.project_id = project_id
        self.role_id = role_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'role_id': self.role_id
        }
