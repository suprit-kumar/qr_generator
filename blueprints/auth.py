"""
Authentication blueprint for user registration, login, and logout
Handles user session management and password hashing
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from models import db, User

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration endpoint
    Validates username, email, and password before creating account
    """
    
    # Redirect if already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required.')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        elif len(username) > 80:
            errors.append('Username must be less than 80 characters.')
        
        if not email:
            errors.append('Email is required.')
        elif '@' not in email or '.' not in email:
            errors.append('Invalid email format.')
        
        if not password:
            errors.append('Password is required.')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        # Check if username exists
        if not errors and User.query.filter_by(username=username).first():
            errors.append('Username already taken. Please choose another.')
        
        # Check if email exists
        if not errors and User.query.filter_by(email=email).first():
            errors.append('Email already registered. Please try logging in.')
        
        # Show errors if validation failed
        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash(f'Account created successfully! Welcome {username}. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during registration: {str(e)}', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login endpoint
    Authenticates user and creates session
    """
    
    # Redirect if already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me', False)
        
        # Validation
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        # Verify password
        if not user or not user.check_password(password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Login user
        login_user(user, remember=remember_me)
        flash(f'Welcome back, {user.username}!', 'success')
        
        # Redirect to next page or dashboard
        next_page = request.args.get('next')
        if not next_page or url_has_allowed_host_and_scheme(next_page):
            next_page = url_for('dashboard.index')
        
        return redirect(next_page)
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout endpoint"""
    username = current_user.username
    logout_user()
    flash(f'You have been logged out. Goodbye, {username}!', 'success')
    return redirect(url_for('auth.login'))


def url_has_allowed_host_and_scheme(url, allowed_hosts=None):
    """
    Validate that URL is safe for redirection
    Prevents open redirect attacks
    
    Args:
        url (str): URL to validate
        allowed_hosts (list): List of allowed hosts
        
    Returns:
        bool: True if URL is safe, False otherwise
    """
    from urllib.parse import urlparse, urlunparse
    
    if allowed_hosts is None:
        allowed_hosts = []
    
    if not url:
        return False
    
    parsed_url = urlparse(url)
    
    # Only allow relative URLs (no scheme and netloc)
    return not parsed_url.scheme and not parsed_url.netloc
