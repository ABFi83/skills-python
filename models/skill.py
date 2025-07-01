from extensions import db
from sqlalchemy.orm import relationship

# Association table for many-to-many relationship between Project and Skill
project_skills = db.Table('project_skills',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

class Skill(db.Model):
    __tablename__ = 'skill'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True, default="")
    short_name = db.Column(db.String(255), nullable=True, default="")
    
    # Relationships
    projects = relationship("Project", secondary=project_skills, back_populates="skills")
    
    def __init__(self, name="", short_name="", projects=None):
        self.name = name
        self.short_name = short_name
        if projects:
            self.projects = projects
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name
        }
