from extension import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class MaintenanceTeams(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    members = db.relationship('User', backref='team', lazy=True)
    equipment_assigned = db.relationship('Equipment', backref='default_team', lazy=True)

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password_hash = db.Column(db.String(2500))
    role = db.Column(db.String(100)) # 'Manager' or 'Technician'
    
    team_id = db.Column(db.Integer, db.ForeignKey('maintenance_teams.team_id'))
    
    requests_assigned = db.relationship('MaintenanceRequest', backref='technician', lazy=True)

    def get_id(self):
        return (self.user_id)

class WorkCentres(db.Model):
    centre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(100))
    cost_per_hour = db.Column(db.Float)
    capacity = db.Column(db.Float)
    
    equipment_list = db.relationship('Equipment', backref='work_centre', lazy=True)

class Equipment(db.Model):
    equipment_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100)) # e.g. 'Machinery', 'Computers'
    purchase_date = db.Column(db.Date)
    warranty_info = db.Column(db.String(250))
    
    department = db.Column(db.String(100)) 
    employee_owner = db.Column(db.String(150)) # If assigned to a specific person
    work_centre_id = db.Column(db.Integer, db.ForeignKey('work_centres.centre_id'))
    
    # Auto-fill Defaults (For "The Breakdown" flow)
    default_team_id = db.Column(db.Integer, db.ForeignKey('maintenance_teams.team_id'))
    default_technician_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    
    # Scrap Logic
    is_scrapped = db.Column(db.Boolean, default=False)
    scrap_date = db.Column(db.DateTime)

    requests = db.relationship('MaintenanceRequest', backref='equipment', lazy=True)

    # Helper for "Smart Button" Badge
    @property
    def request_count(self):
        return MaintenanceRequest.query.filter_by(equipment_id=self.equipment_id).count()

class MaintenanceRequest(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    request_type = db.Column(db.String(50), nullable=False) # 'Corrective' or 'Preventive'
    priority = db.Column(db.String(50), default='Normal')
    stage = db.Column(db.String(50), default='New') # 'New', 'In Progress', 'Repaired', 'Scrap'
    
    # Links
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.equipment_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('maintenance_teams.team_id'))
    technician_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    
    # Timing
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_date = db.Column(db.DateTime) 
    close_date = db.Column(db.DateTime)
    duration_hours = db.Column(db.Float, default=0.0)