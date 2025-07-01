from extensions import db
from sqlalchemy.orm import relationship

class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    
    # Relationships
    user_projects = relationship("UserProject", back_populates="role")
    
    def __init__(self, code, name):
        self.code = code
        self.name = name
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name
        }
