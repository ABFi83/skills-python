from extensions import db
from models.user import User
from sqlalchemy import or_
import bcrypt

class UserService:
    def __init__(self):
        pass
    
    def get_all_users(self, search=None):
        """Retrieve all users with optional search filter"""
        try:
            if search:
                # Filter users whose username contains the search term
                return User.query.filter(User.username.like(f'{search}%')).all()
            else:
                return User.query.all()
        except Exception as e:
            print(f"Error retrieving users: {e}")
            raise Exception("Could not retrieve users")
    
    def create_user(self, user_data):
        """Create a new user"""
        try:
            # Hash the password
            salt_rounds = 10
            hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
            
            user = User(
                name=user_data.get('name'),
                surname=user_data.get('surname'),
                username=user_data['username'],
                password=hashed_password.decode('utf-8'),
                code=user_data['code'],
                is_admin=user_data.get('is_admin', False)
            )
            
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            raise Exception("Could not create user")
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            return User.query.filter_by(id=user_id).first()
        except Exception as e:
            print(f"Error retrieving user: {e}")
            raise Exception("Could not retrieve user")
    
    def get_username_password(self, username):
        """Get user by username for authentication"""
        try:
            return User.query.filter_by(username=username).first()
        except Exception as e:
            print(f"Error retrieving user: {e}")
            raise Exception("Could not retrieve user")
    
    def delete_user(self, user_id):
        """Delete user by ID"""
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                db.session.delete(user)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user: {e}")
            raise Exception("Could not delete user")
