from extensions import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    surname = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=True, default=False)
    
    # Relationships
    user_projects = relationship("UserProject", back_populates="user")
    
    def __init__(self, name=None, surname=None, username=None, password=None, code=None, is_admin=False):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password
        self.code = code
        self.is_admin = is_admin
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'username': self.username,
            'code': self.code,
            'is_admin': self.is_admin
        }
