from flask import Blueprint, request, redirect, flash, render_template, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from extension import db
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def validate_password(password):
    """
    Checking for:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one special character
    """
    if len(password) < 8:
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[ !@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        return False
    return True

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        # 1. Duplicate Email Check
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account with this email already exists.', 'warning')
            return render_template('auth.html', flip_to_signup=True)

        # 2. Password Complexity Check
        if not validate_password(password):
            flash('Password must be >8 chars, contain Upper, Lower, and Special characters.', 'danger')
            return render_template('auth.html', flip_to_signup=True)

        # 3. Create User (Default Role: Portal)
        hashed_pw = generate_password_hash(password)
        new_user = User(
            email=email, 
            name=name, 
            password_hash=hashed_pw,
            role='Portal' 
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth.html', flip_to_signup=True)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        # Specific Error Logic
        if not user:
            flash('Account does not exist.', 'danger')
            return render_template('auth.html', flip_to_signup=False)
            
        if not check_password_hash(user.password_hash, password):
            flash('Invalid Password.', 'danger')
            return render_template('auth.html', flip_to_signup=False)
            
        # Success
        login_user(user)
        
        # Redirect based on role
        if user.role == 'Technician':
            return redirect(url_for('maintenance.kanban_board')) 
        
        # Manager or Portal User -> Dashboard
        return redirect(url_for('main.dashboard')) 

    return render_template('auth.html', flip_to_signup=False)

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('If that email exists, a reset link has been sent.', 'info')
        else:
            flash('Account does not exist.', 'danger')
            
        return redirect(url_for('auth.login'))
        
    return render_template('auth/forgot_password.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))