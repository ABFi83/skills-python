from extensions import db
from sqlalchemy.orm import relationship

class Project(db.Model):
    __tablename__ = 'project'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, default="")
    description = db.Column(db.String(255), nullable=False, default="")
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    
    # Relationships
    user_projects = relationship("UserProject", back_populates="project")
    client = relationship("Client", back_populates="projects")
    skills = relationship("Skill", secondary="project_skills", back_populates="projects")
    evaluations = relationship("Evaluation", back_populates="project", cascade="all, delete-orphan")
    
    def __init__(self, name="", description="", client_id=None):
        self.name = name
        self.description = description
        self.client_id = client_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'client_id': self.client_id
        }
