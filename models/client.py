from extensions import db
from sqlalchemy.orm import relationship

class Client(db.Model):
    __tablename__ = 'client'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), nullable=False)
    file = db.Column(db.String(255), nullable=False)
    
    # Relationships
    projects = relationship("Project", back_populates="client")
    
    def __init__(self, name, code, file):
        self.name = name
        self.code = code
        self.file = file
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'file': self.file
        }
