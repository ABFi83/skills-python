from extensions import db
from sqlalchemy.orm import relationship
from datetime import datetime

class Evaluation(db.Model):
    __tablename__ = 'evaluation'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    close = db.Column(db.Boolean, nullable=True, default=False)
    evaluation_date = db.Column(db.Date, nullable=False)
    
    # Relationships
    user = relationship("User")
    project = relationship("Project", back_populates="evaluations")
    values = relationship("Values", back_populates="evaluation", cascade="all, delete-orphan")
    
    def __init__(self, user_id, project_id, start_date, end_date, evaluation_date, close=False):
        self.user_id = user_id
        self.project_id = project_id
        self.start_date = start_date
        self.end_date = end_date
        self.evaluation_date = evaluation_date
        self.close = close
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'close': self.close,
            'evaluation_date': self.evaluation_date.isoformat() if self.evaluation_date else None
        }
