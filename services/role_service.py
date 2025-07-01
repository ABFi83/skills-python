from extensions import db
from models.role import Role

class RoleService:
    def __init__(self):
        pass
    
    def get_all_roles(self, search=None):
        """Get all roles with optional search filter"""
        try:
            query = Role.query
            if search:
                query = query.filter(Role.name.like(f'%{search}%'))
            return query.all()
        except Exception as e:
            raise Exception(f"Could not retrieve roles: {e}")
    
    def get_role_by_id(self, role_id):
        """Get role by ID"""
        try:
            return Role.query.filter_by(id=role_id).first()
        except Exception as e:
            raise Exception(f"Could not retrieve role: {e}")
    
    def create_role(self, role_data):
        """Create a new role"""
        try:
            role = Role(
                code=role_data.get('code', ''),
                name=role_data.get('name', '')
            )
            db.session.add(role)
            db.session.commit()
            return role
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Could not create role: {e}")
    
    def update_role(self, role_id, role_data):
        """Update an existing role"""
        try:
            role = Role.query.filter_by(id=role_id).first()
            if not role:
                return None
            
            if 'code' in role_data:
                role.code = role_data['code']
            if 'name' in role_data:
                role.name = role_data['name']
            
            db.session.commit()
            return role
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Could not update role: {e}")
    
    def delete_role(self, role_id):
        """Delete role by ID"""
        try:
            role = Role.query.filter_by(id=role_id).first()
            if role:
                db.session.delete(role)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Could not delete role: {e}")
