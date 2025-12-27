from flask import Blueprint, jsonify, request
from models import Equipment, MaintenanceRequest

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/equipment/<int:id>/details')
def get_equipment_details(id):
    equipment = Equipment.query.get_or_404(id)
    response_data = {
        'category': equipment.category,
        'default_team_id': equipment.default_team_id,
        'default_technician_id': equipment.default_technician_id,
        'department': equipment.department
    }
    
    return jsonify(response_data)

@api_bp.route('/calendar/events')
def get_calendar_events():
    events = MaintenanceRequest.query.filter(
        MaintenanceRequest.scheduled_date.isnot(None)
    ).all()
    
    event_list = []
    for req in events:
        color = '#28a745' if req.request_type == 'Preventive' else '#dc3545' # Green for Prev, Red for Corr
        
        event_list.append({
            'id': req.request_id,
            'title': f"{req.equipment.name} - {req.subject}",
            'start': req.scheduled_date.isoformat(), # ISO format (YYYY-MM-DD) is required by JS
            'url': f"/maintenance/request/{req.request_id}", # Optional: Link to details
            'color': color 
        })
        
    return jsonify(event_list)

@api_bp.route('/request/<int:id>/update-stage', methods=['POST'])
def update_request_stage(id):
    """
    Updates the stage when a card is dropped (if using pure AJAX).
    """
    from extension import db
    from datetime import datetime
    
    data = request.get_json()
    new_stage = data.get('stage')
    
    req = MaintenanceRequest.query.get_or_404(id)
    req.stage = new_stage
    
    # Scrap Logic Check [Source: 74-76]
    if new_stage == 'Scrap':
        equipment = Equipment.query.get(req.equipment_id)
        if equipment:
            equipment.is_scrapped = True
            equipment.scrap_date = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Stage updated'})