"""
Main Flask application for QR Code Generator
Entry point for the application with blueprint registration and error handling
"""

import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from config import config
from models import db, User, init_db

# Import blueprints
from blueprints.auth import auth_bp
from blueprints.dashboard import dashboard_bp
from blueprints.qr_generator import qr_bp
from blueprints.history import history_bp


def create_app(config_name=None):
    """
    Application factory function
    
    Args:
        config_name (str): Configuration environment (development, production, testing)
        
    Returns:
        Flask: Configured Flask application
    """
    
    # Determine configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config.get(config_name, config['development']))
    
    # Create upload folders if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['GENERATED_QR_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID"""
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(qr_bp)
    app.register_blueprint(history_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Root route - redirect to dashboard or login
    @app.route('/')
    def index():
        """Root route"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors"""
        return '''
        <div style="text-align: center; margin-top: 50px; font-family: Arial;">
            <h1>404 - Page Not Found</h1>
            <p>The page you're looking for doesn't exist.</p>
            <a href="/">Go Home</a>
        </div>
        ''', 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        db.session.rollback()
        return '''
        <div style="text-align: center; margin-top: 50px; font-family: Arial;">
            <h1>500 - Internal Server Error</h1>
            <p>Something went wrong on our end.</p>
            <a href="/">Go Home</a>
        </div>
        ''', 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 errors"""
        return '''
        <div style="text-align: center; margin-top: 50px; font-family: Arial;">
            <h1>403 - Forbidden</h1>
            <p>You don't have permission to access this resource.</p>
            <a href="/">Go Home</a>
        </div>
        ''', 403
    
    # CLI commands for database management
    @app.cli.command()
    def init_database():
        """Initialize the database"""
        init_db(app)
    
    @app.cli.command()
    def create_admin():
        """Create admin user for testing"""
        from getpass import getpass
        username = input('Enter admin username: ')
        email = input('Enter admin email: ')
        password = getpass('Enter admin password: ')
        
        if User.query.filter_by(username=username).first():
            print('Username already exists!')
            return
        
        admin = User(username=username, email=email)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f'Admin user {username} created successfully!')
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
