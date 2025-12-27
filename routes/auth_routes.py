from flask import Blueprint, request, redirect, flash, render_template, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, MaintenanceTeams
from extension import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password)

        new_user = User(
            email=email, 
            name=name, 
            password_hash=hashed_pw, 
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Please login.', 'success')
        return redirect(url_for('auth.login'))

    teams = MaintenanceTeams.query.all()
    return render_template('auth.html', teams=teams)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.role == 'Manager':
                return redirect(url_for('main.dashboard')) 
            elif user.role == 'Technician':
                return redirect(url_for('maintenance.kanban_board')) 
            else:
                return redirect(url_for('main.dashboard'))
                
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('auth.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))