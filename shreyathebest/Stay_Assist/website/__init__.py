import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Secret key and database configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Set Upload Folder Path
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

    # Ensure the Upload Folder Exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Configure login manager
    login_manager.login_view = 'auth.sign_in'  # Route for login page
    login_manager.login_message_category = 'info'

    # Import blueprints AFTER app creation to avoid circular imports
    with app.app_context():
        from .auth import auth
        from .views import views
        
        app.register_blueprint(auth, url_prefix='/')
        app.register_blueprint(views, url_prefix='/')

        # Create database tables if they don't exist
        db.create_all()

    return app
