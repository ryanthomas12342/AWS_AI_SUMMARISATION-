from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions with app
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.upload import upload_bp
    from app.routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(upload_bp, url_prefix='/upload')
    
    # Create database tables
    
    
    return app 