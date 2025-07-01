from extensions import db
from models.skill import Skill

class SkillService:
    def __init__(self):
        pass
    
    def get_all_skills(self, search=None):
        """Retrieve all skills with optional search filter"""
        try:
            if search:
                return Skill.query.filter(Skill.name.like(f'{search}%')).all()
            else:
                return Skill.query.all()
        except Exception as e:
            print(f"Error retrieving skills: {e}")
            raise Exception("Could not retrieve skills")
    
    def get_skill_by_id(self, skill_id):
        """Get skill by ID"""
        try:
            return Skill.query.filter_by(id=skill_id).first()
        except Exception as e:
            print(f"Error retrieving skill: {e}")
            raise Exception("Could not retrieve skill")
    
    def create_skill(self, skill_data):
        """Create a new skill"""
        try:
            skill = Skill(
                name=skill_data.get('name', ''),
                short_name=skill_data.get('short_name', '')
            )
            
            db.session.add(skill)
            db.session.commit()
            return skill
        except Exception as e:
            db.session.rollback()
            print(f"Error creating skill: {e}")
            raise Exception("Could not create skill")
    
    def delete_skill(self, skill_id):
        """Delete skill by ID"""
        try:
            skill = Skill.query.filter_by(id=skill_id).first()
            if skill:
                db.session.delete(skill)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting skill: {e}")
            raise Exception("Could not delete skill")
