"""
Configuration module for QR Code Generator application
Handles database, secret key, and app settings
"""

import os
from datetime import timedelta


class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    GENERATED_QR_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'generated_qr')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # QR Code settings
    QR_DEFAULT_VERSION = 1
    QR_ERROR_CORRECTION = 'H'
    QR_BOX_SIZE = 10
    QR_BORDER = 4


class DevelopmentConfig(Config):
    """Development configuration"""
    
    DEBUG = True
    SQLALCHEMY_ECHO = True
    # SQLite database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///qr_generator.db'


class ProductionConfig(Config):
    """Production configuration"""
    
    DEBUG = False
    # MySQL database (uncomment and configure for MySQL)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'mysql+pymysql://user:password@localhost/qr_generator_db'
    
    # SQLite fallback for production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///qr_generator.db'


class TestingConfig(Config):
    """Testing configuration"""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
