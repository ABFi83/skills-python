from extensions import db
from sqlalchemy.orm import relationship

class Values(db.Model):
    __tablename__ = 'values'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluation.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    
    # Relationships
    skill = relationship("Skill")
    evaluation = relationship("Evaluation", back_populates="values")
    
    def __init__(self, skill_id, evaluation_id, value):
        self.skill_id = skill_id
        self.evaluation_id = evaluation_id
        self.value = value
    
    def to_dict(self):
        return {
            'id': self.id,
            'skill_id': self.skill_id,
            'evaluation_id': self.evaluation_id,
            'value': self.value
        }
