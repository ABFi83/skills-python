from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler('app.log')  # Output to file
    ]
)

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'YOUR_SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'YOUR_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///mydb.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    from extensions import db, jwt, cors, bcrypt
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)
    
    # Import models (after extensions are initialized)
    from models.user import User
    from models.skill import Skill
    from models.project import Project
    from models.client import Client
    from models.role import Role
    from models.evaluation import Evaluation
    from models.userproject import UserProject
    from models.values import Values
    
    # Import and register blueprints
    from controllers.users_controller import users_bp
    from controllers.skills_controller import skills_bp
    from controllers.projects_controller import projects_bp
    from controllers.evaluations_controller import evaluations_bp
    from controllers.token_controller import token_bp
    from controllers.init_controller import init_bp
    from controllers.client_controller import client_bp
    from controllers.role_controller import role_bp
    from controllers.get_evaluations_controller import get_evaluations_bp
    
    app.register_blueprint(users_bp)
    app.register_blueprint(skills_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(evaluations_bp)
    app.register_blueprint(token_bp)
    app.register_blueprint(init_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(get_evaluations_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
