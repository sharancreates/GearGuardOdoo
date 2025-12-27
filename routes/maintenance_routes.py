from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extension import db
from models import MaintenanceRequest, Equipment, MaintenanceTeams, User
from datetime import datetime

maintenance_bp = Blueprint('maintenance', __name__, url_prefix='/maintenance')

@maintenance_bp.route('/kanban')
@login_required
def kanban_board():
    new_reqs = MaintenanceRequest.query.filter_by(stage='New').all()
    progress_reqs = MaintenanceRequest.query.filter_by(stage='In Progress').all()
    repaired_reqs = MaintenanceRequest.query.filter_by(stage='Repaired').all()
    scrap_reqs = MaintenanceRequest.query.filter_by(stage='Scrap').all()

    return render_template('maintenance/kanban.html',
                           new_reqs=new_reqs,
                           progress_reqs=progress_reqs,
                           repaired_reqs=repaired_reqs,
                           scrap_reqs=scrap_reqs)

@maintenance_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_request():
    if request.method == 'POST':
        subject = request.form.get('subject')
        description = request.form.get('description')
        req_type = request.form.get('request_type') # 'Corrective' or 'Preventive'
        priority = request.form.get('priority')
        equipment_id = request.form.get('equipment_id')
        
        # Auto-filled fields (hidden inputs or user selection)
        team_id = request.form.get('team_id') 
        technician_id = request.form.get('technician_id')

        # Date Handling
        scheduled_date = None
        s_date_str = request.form.get('scheduled_date')
        if s_date_str:
            scheduled_date = datetime.strptime(s_date_str, '%Y-%m-%d').date()

        # Create Object
        new_req = MaintenanceRequest(
            subject=subject,
            description=description,
            request_type=req_type,
            priority=priority,
            stage='New', # Default stage
            equipment_id=equipment_id,
            team_id=team_id,
            technician_id=technician_id,
            scheduled_date=scheduled_date
        )

        db.session.add(new_req)
        db.session.commit()
        
        flash('Request created successfully!', 'success')
        
        # Redirect based on type: Preventive -> Calendar, Corrective -> Kanban
        if req_type == 'Preventive':
            return redirect(url_for('maintenance.calendar_view'))
        return redirect(url_for('maintenance.kanban_board'))

    # GET: Load dropdowns
    equipment_list = Equipment.query.filter_by(is_scrapped=False).all() # Don't show scrapped items
    teams = MaintenanceTeams.query.all()
    users = User.query.all()

    return render_template('maintenance/request_form.html', 
                           equipment_list=equipment_list,
                           teams=teams,
                           users=users)

# --- 3. UPDATE STAGE / MOVE CARD ---
@maintenance_bp.route('/update_stage/<int:request_id>/<string:new_stage>')
@login_required
def update_stage(request_id, new_stage):
    """
    Handles Drag & Drop logic.
    CRITICAL: Implements 'Scrap Logic' [Source: 74-76].
    """
    req = MaintenanceRequest.query.get_or_404(request_id)
    
    # 1. Update the stage
    req.stage = new_stage
    
    # 2. Handle Duration (If moving to Repaired)
    if new_stage == 'Repaired':
        req.close_date = datetime.utcnow()
        # In a real app, you might calculate duration here or ask via a modal
    
    # 3. SCRAP LOGIC: If moved to Scrap, mark Equipment as unusable
    if new_stage == 'Scrap':
        equipment = Equipment.query.get(req.equipment_id)
        if equipment:
            equipment.is_scrapped = True
            equipment.scrap_date = datetime.utcnow()
            flash(f'Warning: Equipment "{equipment.name}" has been marked as SCRAPPED.', 'warning')

    db.session.commit()
    
    # If called via AJAX (from Kanban), return JSON
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'success', 'new_stage': new_stage})
        
    return redirect(url_for('maintenance.kanban_board'))

# --- 4. CALENDAR VIEW ---
@maintenance_bp.route('/calendar')
@login_required
def calendar_view():
    """
    Displays Preventive Maintenance schedule.
    Source: [61-63]
    """
    return render_template('maintenance/calendar.html')

# --- 5. SMART BUTTON LIST VIEW ---
@maintenance_bp.route('/history/<int:equipment_id>')
@login_required
def list_requests(equipment_id):
    """
    The destination for the 'Smart Button' on the Equipment form.
    Source: [72] "Opens a list of all requests related only to that specific machine."
    """
    equipment = Equipment.query.get_or_404(equipment_id)
    requests = MaintenanceRequest.query.filter_by(equipment_id=equipment_id).all()
    
    return render_template('maintenance/history_list.html', 
                           equipment=equipment, 
                           requests=requests)