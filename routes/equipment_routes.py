from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extension import db
from models import Equipment, WorkCentres, MaintenanceTeams, User
from datetime import datetime

equipment_bp = Blueprint('equipment', __name__, url_prefix='/equipment')

@equipment_bp.route('/')
@login_required
def list_equipment():

    search_query = request.args.get('search')
    if search_query:
        all_equipment = Equipment.query.filter(
            (Equipment.name.ilike(f'%{search_query}%')) | 
            (Equipment.serial_number.ilike(f'%{search_query}%'))
        ).all()
    else:
        all_equipment = Equipment.query.all()
        
    return render_template('equipment/list.html', equipment=all_equipment)

@equipment_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_equipment():
    if request.method == 'POST':
        name = request.form.get('name')
        serial = request.form.get('serial_number')
        category = request.form.get('category')
        purchase_date_str = request.form.get('purchase_date')
        
        # Validation: Check Duplicate Serial
        existing = Equipment.query.filter_by(serial_number=serial).first()
        if existing:
            flash(f'Serial Number "{serial}" already exists!', 'warning')
            return redirect(url_for('equipment.new_equipment'))

        purchase_date = None
        if purchase_date_str:
            purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d').date()

        new_item = Equipment(
            name=name,
            serial_number=serial,
            category=category,
            purchase_date=purchase_date,
            warranty_info=request.form.get('warranty_info'),
            department=request.form.get('department'),
            employee_owner=request.form.get('employee_owner'),
            work_centre_id=request.form.get('work_centre_id'),
            default_team_id=request.form.get('default_team_id'),
            default_technician_id=request.form.get('default_technician_id')
        )

        try:
            db.session.add(new_item)
            db.session.commit()
            flash('Equipment added successfully!', 'success')
            return redirect(url_for('equipment.list_equipment'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding equipment: {str(e)}', 'danger')

    work_centres = WorkCentres.query.all()
    teams = MaintenanceTeams.query.all()
    users = User.query.all() 

    return render_template('equipment/form.html', 
                           work_centres=work_centres, 
                           teams=teams, 
                           users=users)

@equipment_bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_equipment(id):

    equipment = Equipment.query.get_or_404(id)

    if request.method == 'POST':
        new_serial = request.form.get('serial_number')
        
        # Validation: Check Duplicate Serial (excluding self)
        existing = Equipment.query.filter(Equipment.serial_number == new_serial, Equipment.equipment_id != id).first()
        if existing:
            flash(f'Serial Number "{new_serial}" is already used by another equipment!', 'warning')
            return redirect(url_for('equipment.edit_equipment', id=id))

        equipment.name = request.form.get('name')
        equipment.serial_number = new_serial
        equipment.category = request.form.get('category')
        equipment.warranty_info = request.form.get('warranty_info')
        
        equipment.work_centre_id = request.form.get('work_centre_id')
        equipment.default_team_id = request.form.get('default_team_id')
        equipment.default_technician_id = request.form.get('default_technician_id')

        p_date = request.form.get('purchase_date')
        if p_date:
            equipment.purchase_date = datetime.strptime(p_date, '%Y-%m-%d').date()

        db.session.commit()
        flash('Equipment updated!', 'success')
        return redirect(url_for('equipment.list_equipment'))

    work_centres = WorkCentres.query.all()
    teams = MaintenanceTeams.query.all()
    users = User.query.all()

    return render_template('equipment/form.html', 
                           equipment=equipment, 
                           work_centres=work_centres, 
                           teams=teams, 
                           users=users)

# --- 4. DELETE EQUIPMENT ---
@equipment_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_equipment(id):
    equipment = Equipment.query.get_or_404(id)
    
    if equipment.requests:
        flash('Cannot delete equipment with existing maintenance requests. Archive/Scrap it instead.', 'warning')
        return redirect(url_for('equipment.list_equipment'))

    db.session.delete(equipment)
    db.session.commit()
    flash('Equipment deleted.', 'info')
    return redirect(url_for('equipment.list_equipment'))