from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.config import Config
import os

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # JWT Configuration for cookies
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
    
    # Initialize extensions with app
    CORS(app, supports_credentials=True)  # Enable credentials in CORS
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.upload import upload_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.summaries import summaries_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(upload_bp, url_prefix='/upload')
    app.register_blueprint(summaries_bp, url_prefix='/summaries')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 