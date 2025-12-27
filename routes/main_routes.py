from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import MaintenanceRequest, Equipment, User

main_bp = Blueprint('main', __name__, url_prefix='/main')

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    
    total_active = MaintenanceRequest.query.filter(
        MaintenanceRequest.stage.in_(['New', 'In Progress'])
    ).count()

    corrective_count = MaintenanceRequest.query.filter_by(
        request_type='Corrective'
    ).filter(MaintenanceRequest.stage.in_(['New', 'In Progress'])).count()

    preventive_count = MaintenanceRequest.query.filter_by(
        request_type='Preventive'
    ).filter(MaintenanceRequest.stage.in_(['New', 'In Progress'])).count()

    my_tasks = MaintenanceRequest.query.filter_by(
        technician_id=current_user.user_id
    ).filter(
        MaintenanceRequest.stage.in_(['New', 'In Progress'])
    ).all()
    
    my_task_count = len(my_tasks)

    recent_activity = MaintenanceRequest.query.order_by(
        MaintenanceRequest.created_at.desc()
    ).limit(5).all()

    scrapped_count = Equipment.query.filter_by(is_scrapped=True).count()

    return render_template('dashboard.html',
                           total_active=total_active,
                           corrective_count=corrective_count,
                           preventive_count=preventive_count,
                           my_tasks=my_tasks,
                           my_task_count=my_task_count,
                           recent_activity=recent_activity,
                           scrapped_count=scrapped_count)