from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extension import db
from models import MaintenanceRequest, Equipment, MaintenanceTeams, User
from datetime import datetime

maintenance_bp = Blueprint('maintenance', __name__, url_prefix='/maintenance')


# -------------------------------
# KANBAN BOARD
# -------------------------------
@maintenance_bp.route('/kanban')
@login_required
def kanban_board():
    return render_template(
        'maintenance/kanban.html',
        new_reqs=MaintenanceRequest.query.filter_by(stage='New').all(),
        progress_reqs=MaintenanceRequest.query.filter_by(stage='In Progress').all(),
        repaired_reqs=MaintenanceRequest.query.filter_by(stage='Repaired').all(),
        scrap_reqs=MaintenanceRequest.query.filter_by(stage='Scrap').all()
    )


# -------------------------------
# NEW REQUEST
# -------------------------------
@maintenance_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_request():
    if request.method == 'POST':
        s_date = request.form.get('scheduled_date')
        scheduled_date = (
            datetime.strptime(s_date, '%Y-%m-%d').date()
            if s_date else None
        )

        new_req = MaintenanceRequest(
            subject=request.form.get('subject'),
            description=request.form.get('description'),
            request_type=request.form.get('request_type'),
            priority=request.form.get('priority'),
            stage='New',
            equipment_id=request.form.get('equipment_id'),
            team_id=request.form.get('team_id'),
            technician_id=request.form.get('technician_id'),
            scheduled_date=scheduled_date
        )

        db.session.add(new_req)
        db.session.commit()

        flash('Request created successfully!', 'success')

        if new_req.request_type == 'Preventive':
            return redirect(url_for('maintenance.calendar_view'))

        return redirect(url_for('maintenance.kanban_board'))

    return render_template(
        'maintenance/request_form.html',
        equipment_list=Equipment.query.filter_by(is_scrapped=False).all(),
        teams=MaintenanceTeams.query.all(),
        users=User.query.all()
    )


# ======================================================
# SHARED STAGE UPDATE LOGIC (IMPORTANT)
# ======================================================
def _apply_stage_change(req: MaintenanceRequest, new_stage: str):
    req.stage = new_stage

    # If repaired → close date
    if new_stage == 'Repaired':
        req.close_date = datetime.utcnow()

    # Scrap logic
    if new_stage == 'Scrap' and req.equipment_id:
        equipment = Equipment.query.get(req.equipment_id)
        if equipment and not equipment.is_scrapped:
            equipment.is_scrapped = True
            equipment.scrap_date = datetime.utcnow()

    db.session.commit()


# -------------------------------
# CLASSIC ROUTE (LINK / REDIRECT)
# -------------------------------
@maintenance_bp.route('/update_stage/<int:request_id>/<string:new_stage>')
@login_required
def update_stage(request_id, new_stage):
    req = MaintenanceRequest.query.get_or_404(request_id)

    _apply_stage_change(req, new_stage)

    flash(f'Request moved to {new_stage}', 'success')
    return redirect(url_for('maintenance.kanban_board'))


# -------------------------------
# AJAX API (KANBAN DRAG & DROP)
# -------------------------------
@maintenance_bp.route('/api/update_stage', methods=['POST'])
@login_required
def update_stage_api():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid payload'}), 400

    request_id = data.get('request_id')
    new_stage = data.get('new_stage')

    if not request_id or not new_stage:
        return jsonify({'error': 'Missing parameters'}), 400

    req = MaintenanceRequest.query.get_or_404(request_id)

    _apply_stage_change(req, new_stage)

    return jsonify({
        'status': 'success',
        'request_id': request_id,
        'new_stage': new_stage
    })


# -------------------------------
# CALENDAR VIEW
# -------------------------------
@maintenance_bp.route('/calendar')
@login_required
def calendar_view():
    return render_template('maintenance/calendar.html')


# -------------------------------
# EQUIPMENT HISTORY
# -------------------------------
@maintenance_bp.route('/history/<int:equipment_id>')
@login_required
def list_requests(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    requests = MaintenanceRequest.query.filter_by(equipment_id=equipment_id).all()

    return render_template(
        'maintenance/history_list.html',
        equipment=equipment,
        requests=requests
    )
