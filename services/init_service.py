from extensions import db
from models.user import User
from models.project import Project
from models.skill import Skill
from models.client import Client
from models.role import Role
from models.userproject import UserProject
from models.evaluation import Evaluation
from models.values import Values
from datetime import datetime, date

class InitService:
    def __init__(self):
        pass
    
    def create_project(self):
        """Create initial project with users, skills, and relationships - COMPLETE VERSION"""
        try:
            # Get users with relations
            user = User.query.filter_by(id=1).first()
            if not user:
                raise Exception("Utente non trovato!")
            
            user1 = User.query.filter_by(id=2).first()
            if not user1:
                raise Exception("Utente non trovato!")
            
            user_lm = User.query.filter_by(id=3).first()
            if not user_lm:
                raise Exception("Utente non trovato!")
            
            # Create or get clients
            client = Client.query.filter_by(code="LUM").first()
            if not client:
                client = Client(
                    name="Lumon",
                    code="LUM",
                    file="LUM.jpg"
                )
                db.session.add(client)
                db.session.commit()
            
            client2 = Client.query.filter_by(code="POH").first()
            if not client2:
                client2 = Client(
                    name="Pollo Hermanos",
                    code="POH",
                    file="POH.jpg"
                )
                db.session.add(client2)
                db.session.commit()
            
            # Create or get skills
            skill1 = Skill.query.filter_by(name="JavaScript").first()
            if not skill1:
                skill1 = Skill(name="JavaScript", short_name="JS")
                db.session.add(skill1)
                db.session.commit()
            
            skill2 = Skill.query.filter_by(name="TypeScript").first()
            if not skill2:
                skill2 = Skill(name="TypeScript", short_name="TS")
                db.session.add(skill2)
                db.session.commit()
            
            skill4 = Skill.query.filter_by(name="Java").first()
            if not skill4:
                skill4 = Skill(name="Java", short_name="JA")
                db.session.add(skill4)
                db.session.commit()
            
            # Create or get roles
            role = Role.query.filter_by(name="Team Leader").first()
            if not role:
                role = Role(code="TL", name="Team Leader")
                db.session.add(role)
                db.session.commit()
            
            role1 = Role.query.filter_by(name="Developer").first()
            if not role1:
                role1 = Role(code="DV", name="Developer")
                db.session.add(role1)
                db.session.commit()
            
            role_lm = Role.query.filter_by(name="Line Manager").first()
            if not role_lm:
                role_lm = Role(code="LM", name="Line Manager")
                db.session.add(role_lm)
                db.session.commit()
            
            # === CREATE FIRST PROJECT ===
            new_project = Project(
                name="Lumon - Scissione",
                description="Avanti ad oltranza"
            )
            new_project.client = client
            new_project.skills = [skill1, skill2, skill4]
            db.session.add(new_project)
            db.session.commit()
            
            # Create user-project relationships for first project
            user_project = UserProject(
                user_id=user.id,
                project_id=new_project.id,
                role_id=role.id
            )
            db.session.add(user_project)
            
            user_project1 = UserProject(
                user_id=user1.id,
                project_id=new_project.id,
                role_id=role1.id
            )
            db.session.add(user_project1)
            
            user_project_lm = UserProject(
                user_id=user_lm.id,
                project_id=new_project.id,
                role_id=role_lm.id
            )
            db.session.add(user_project_lm)
            db.session.commit()
            
            # === CREATE EVALUATIONS FOR FIRST PROJECT ===
            
            # User 1 - Recent evaluation (2024-02-28)
            evaluation = Evaluation(
                evaluation_date=date(2024, 2, 28),
                user_id=user.id,
                project_id=new_project.id,
                start_date=date(2024, 2, 1),
                end_date=date(2024, 2, 28),
                close=True
            )
            db.session.add(evaluation)
            db.session.commit()
            
            # Values for recent evaluation - User 1
            value = Values(
                skill_id=skill1.id,
                value=10,
                evaluation_id=evaluation.id
            )
            db.session.add(value)
            
            value1 = Values(
                skill_id=skill2.id,
                value=5,
                evaluation_id=evaluation.id
            )
            db.session.add(value1)
            
            value4 = Values(
                skill_id=skill4.id,
                value=8,
                evaluation_id=evaluation.id
            )
            db.session.add(value4)
            
            # User 1 - Old evaluation (2024-01-31)
            evaluation_old = Evaluation(
                evaluation_date=date(2024, 1, 31),
                user_id=user.id,
                project_id=new_project.id,
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 31),
                close=True
            )
            db.session.add(evaluation_old)
            db.session.commit()
            
            # Values for old evaluation - User 1
            value_old = Values(
                skill_id=skill1.id,
                value=7,
                evaluation_id=evaluation_old.id
            )
            db.session.add(value_old)
            
            value_old1 = Values(
                skill_id=skill2.id,
                value=9,
                evaluation_id=evaluation_old.id
            )
            db.session.add(value_old1)
            
            value_old2 = Values(
                skill_id=skill4.id,
                value=2,
                evaluation_id=evaluation_old.id
            )
            db.session.add(value_old2)
            
            # User 2 - Recent evaluation (2024-02-28)
            evaluation1 = Evaluation(
                evaluation_date=date(2024, 2, 28),
                user_id=user1.id,
                project_id=new_project.id,
                start_date=date(2024, 2, 28),
                end_date=date(2024, 2, 28),
                close=True
            )
            db.session.add(evaluation1)
            db.session.commit()
            
            # Values for User 2 recent evaluation
            value_sn = Values(
                skill_id=skill1.id,
                value=2,
                evaluation_id=evaluation1.id
            )
            db.session.add(value_sn)
            
            value_sn1 = Values(
                skill_id=skill2.id,
                value=3,
                evaluation_id=evaluation1.id
            )
            db.session.add(value_sn1)
            
            value_sn4 = Values(
                skill_id=skill4.id,
                value=4,
                evaluation_id=evaluation1.id
            )
            db.session.add(value_sn4)
            
            # User 2 - Old evaluation (2024-01-31)
            evaluation_old_sn = Evaluation(
                evaluation_date=date(2024, 1, 31),
                user_id=user1.id,
                project_id=new_project.id,
                start_date=date(2024, 1, 31),
                end_date=date(2024, 1, 31),
                close=True
            )
            db.session.add(evaluation_old_sn)
            db.session.commit()
            
            # Values for User 2 old evaluation
            value_old_sn = Values(
                skill_id=skill1.id,
                value=7,
                evaluation_id=evaluation_old_sn.id
            )
            db.session.add(value_old_sn)
            
            value_old_sn1 = Values(
                skill_id=skill2.id,
                value=9,
                evaluation_id=evaluation_old_sn.id
            )
            db.session.add(value_old_sn1)
            
            value_old_sn2 = Values(
                skill_id=skill4.id,
                value=2,
                evaluation_id=evaluation_old_sn.id
            )
            db.session.add(value_old_sn2)
            
            # === CREATE SECOND PROJECT ===
            new_project2 = Project(
                name="Pollo Hermanos - Icemberg",
                description="Breaking"
            )
            new_project2.client = client2
            new_project2.skills = [skill1, skill2, skill4]
            db.session.add(new_project2)
            db.session.commit()
            
            # Create user-project relationships for second project
            user_project3 = UserProject(
                user_id=user.id,
                project_id=new_project2.id,
                role_id=role.id
            )
            db.session.add(user_project3)
            
            user_project_lm2 = UserProject(
                user_id=user_lm.id,
                project_id=new_project2.id,
                role_id=role_lm.id
            )
            db.session.add(user_project_lm2)
            db.session.commit()
            
            # === CREATE EVALUATION FOR SECOND PROJECT ===
            evaluation_np2 = Evaluation(
                evaluation_date=date(2024, 1, 28),
                user_id=user.id,
                project_id=new_project2.id,
                start_date=date(2024, 1, 28),
                end_date=date(2024, 1, 28),
                close=True
            )
            db.session.add(evaluation_np2)
            db.session.commit()
            
            # Values for second project evaluation
            value_np2 = Values(
                skill_id=skill1.id,
                value=10,
                evaluation_id=evaluation_np2.id
            )
            db.session.add(value_np2)
            
            value1_np2 = Values(
                skill_id=skill2.id,
                value=5,
                evaluation_id=evaluation_np2.id
            )
            db.session.add(value1_np2)
            
            value4_np2 = Values(
                skill_id=skill4.id,
                value=8,
                evaluation_id=evaluation_np2.id
            )
            db.session.add(value4_np2)
            
            # Final commit
            db.session.commit()
            
            return [new_project.id, new_project2.id]
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating project: {e}")
            raise Exception("Could not create project")
