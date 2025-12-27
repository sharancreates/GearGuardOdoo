from app import create_app
from extension import db
from models import MaintenanceTeams, WorkCentres, User, Equipment, MaintenanceRequest
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    # 1. Clear existing data
    db.drop_all()
    db.create_all()
    print(">>> Database cleared and recreated.")

    # 2. Create Maintenance Teams
    team_mech = MaintenanceTeams(name="Mechanics")
    team_it = MaintenanceTeams(name="IT Support")
    team_elec = MaintenanceTeams(name="Electrical")
    team_facility = MaintenanceTeams(name="Facility Mgmt")
    
    db.session.add_all([team_mech, team_it, team_elec, team_facility])
    db.session.commit()
    print(">>> Teams created.")

    # 3. Create Work Centers (Locations)
    wc_assembly = WorkCentres(name="Assembly Line A", code="AL-01", cost_per_hour=120.0, capacity=100)
    wc_drill = WorkCentres(name="Drill Station 1", code="DS-01", cost_per_hour=45.50, capacity=50)
    wc_server = WorkCentres(name="Server Room B", code="SR-02", cost_per_hour=200.0, capacity=10)
    wc_pack = WorkCentres(name="Packaging Unit", code="PKG-05", cost_per_hour=85.00, capacity=80)
    wc_office = WorkCentres(name="Admin Office", code="OFF-01", cost_per_hour=20.00, capacity=20)

    db.session.add_all([wc_assembly, wc_drill, wc_server, wc_pack, wc_office])
    db.session.commit()
    print(">>> Work Centers created.")

    # 4. Create Users
    password = generate_password_hash("password123")
    
    mgr = User(name="manager", email="manager@gearguard.com", password_hash=password, role="Manager")
    
    # Technicians
    tech_john = User(name="john_mech", email="john@gearguard.com", password_hash=password, role="Technician", team_id=team_mech.team_id)
    tech_sarah = User(name="sarah_it", email="sarah@gearguard.com", password_hash=password, role="Technician", team_id=team_it.team_id)
    tech_mike = User(name="mike_elec", email="mike@gearguard.com", password_hash=password, role="Technician", team_id=team_elec.team_id)
    tech_dave = User(name="dave_fac", email="dave@gearguard.com", password_hash=password, role="Technician", team_id=team_facility.team_id)
    tech_jen = User(name="jen_mech", email="jen@gearguard.com", password_hash=password, role="Technician", team_id=team_mech.team_id)

    db.session.add_all([mgr, tech_john, tech_sarah, tech_mike, tech_dave, tech_jen])
    db.session.commit()
    print(">>> Users created (Login: manager@gearguard.com / password123)")

    # 5. Create Equipment (12 Items)
    equipment_list = [
        # Mechanics Equipment
        Equipment(name="CNC Milling Machine", serial_number="CNC-998877", category="Heavy Machinery", work_centre_id=wc_assembly.centre_id, default_team_id=team_mech.team_id, default_technician_id=tech_john.user_id, department="Production", purchase_date=datetime(2022, 5, 10)),
        Equipment(name="Hydraulic Press 50T", serial_number="HYD-112233", category="Heavy Machinery", work_centre_id=wc_assembly.centre_id, default_team_id=team_mech.team_id, default_technician_id=tech_john.user_id, department="Production", purchase_date=datetime(2020, 11, 5)),
        Equipment(name="Industrial Drill Press", serial_number="DRL-554422", category="Machinery", work_centre_id=wc_drill.centre_id, default_team_id=team_mech.team_id, default_technician_id=tech_jen.user_id, department="Production", purchase_date=datetime(2021, 2, 20)),
        
        # IT Equipment
        Equipment(name="Dell PowerEdge Server", serial_number="SRV-554433", category="Computers", work_centre_id=wc_server.centre_id, default_team_id=team_it.team_id, default_technician_id=tech_sarah.user_id, department="IT", purchase_date=datetime(2023, 6, 10)),
        Equipment(name="Network Switch Cisco", serial_number="NET-990011", category="Network", work_centre_id=wc_server.centre_id, default_team_id=team_it.team_id, default_technician_id=tech_sarah.user_id, department="IT", purchase_date=datetime(2023, 1, 15)),
        Equipment(name="Admin Printer Lrg", serial_number="PRT-009988", category="Peripherals", work_centre_id=wc_office.centre_id, default_team_id=team_it.team_id, default_technician_id=tech_sarah.user_id, department="Admin", purchase_date=datetime(2021, 9, 12)),
        
        # Electrical Equipment
        Equipment(name="Conveyor Belt Motor", serial_number="MTR-776655", category="Electrical", work_centre_id=wc_pack.centre_id, default_team_id=team_elec.team_id, default_technician_id=tech_mike.user_id, department="Logistics", purchase_date=datetime(2022, 3, 20)),
        Equipment(name="Generator Backup A", serial_number="GEN-123456", category="Electrical", work_centre_id=wc_assembly.centre_id, default_team_id=team_elec.team_id, default_technician_id=tech_mike.user_id, department="Facility", purchase_date=datetime(2019, 8, 30)),
        
        # Facility Equipment
        Equipment(name="Forklift Toyota", serial_number="FL-445566", category="Vehicle", work_centre_id=wc_pack.centre_id, default_team_id=team_facility.team_id, default_technician_id=tech_dave.user_id, department="Logistics", purchase_date=datetime(2020, 4, 1)),
        Equipment(name="HVAC Unit Roof", serial_number="HVAC-001122", category="Facility", work_centre_id=wc_office.centre_id, default_team_id=team_facility.team_id, default_technician_id=tech_dave.user_id, department="Facility", purchase_date=datetime(2018, 12, 5)),
        
        # Others
        Equipment(name="3D Printer Prusa", serial_number="3DP-X100", category="Prototyping", work_centre_id=wc_drill.centre_id, default_team_id=team_it.team_id, default_technician_id=tech_sarah.user_id, department="R&D", purchase_date=datetime(2024, 1, 10)),
        Equipment(name="Coffee Machine", serial_number="COF-999", category="Kitchen", work_centre_id=wc_office.centre_id, default_team_id=team_facility.team_id, default_technician_id=tech_dave.user_id, department="HR", purchase_date=datetime(2023, 11, 25))
    ]

    db.session.add_all(equipment_list)
    db.session.commit()
    print(">>> Equipment created (12 items).")

    # 6. Create Maintenance Requests (So the dashboard isn't empty)
    # We need to fetch the IDs we just created
    reqs = [
        # Breakdown - In Progress
        MaintenanceRequest(subject="Leaking Oil", description="Oil puddle found under gearbox.", request_type="Corrective", priority="High", stage="In Progress", equipment_id=1, team_id=team_mech.team_id, technician_id=tech_john.user_id, created_at=datetime.now() - timedelta(days=2)),
        
        # Preventive - Scheduled Future
        MaintenanceRequest(subject="Quarterly Service", description="Routine filter change.", request_type="Preventive", priority="Normal", stage="New", equipment_id=1, team_id=team_mech.team_id, technician_id=tech_john.user_id, scheduled_date=datetime.now() + timedelta(days=5)),
        
        # IT Issue - New
        MaintenanceRequest(subject="Server Overheating", description="Fans making loud noise.", request_type="Corrective", priority="High", stage="New", equipment_id=4, team_id=team_it.team_id, technician_id=tech_sarah.user_id, created_at=datetime.now() - timedelta(hours=4)),
        
        # Electrical - Repaired
        MaintenanceRequest(subject="Motor Fuse Blown", description="Replaced main fuse.", request_type="Corrective", priority="High", stage="Repaired", equipment_id=7, team_id=team_elec.team_id, technician_id=tech_mike.user_id, created_at=datetime.now() - timedelta(days=10), duration_hours=2.5),
        
        # Facility - New
        MaintenanceRequest(subject="Forklift Tire Flat", description="Rear left tire needs replacement.", request_type="Corrective", priority="Normal", stage="New", equipment_id=9, team_id=team_facility.team_id, technician_id=tech_dave.user_id),
        
        # Preventive - Calendar Event
        MaintenanceRequest(subject="Generator Test", description="Annual load test.", request_type="Preventive", priority="High", stage="New", equipment_id=8, team_id=team_elec.team_id, technician_id=tech_mike.user_id, scheduled_date=datetime.now() + timedelta(days=2)),
        
        # Scrap Item
        MaintenanceRequest(subject="Coffee Machine Broken", description="Heating element dead. Too expensive to fix.", request_type="Corrective", priority="Low", stage="Scrap", equipment_id=12, team_id=team_facility.team_id, technician_id=tech_dave.user_id),
        
        # Another In Progress
        MaintenanceRequest(subject="Printer Jamming", description="Paper stuck in roller.", request_type="Corrective", priority="Normal", stage="In Progress", equipment_id=6, team_id=team_it.team_id, technician_id=tech_sarah.user_id)
    ]

    db.session.add_all(reqs)
    db.session.commit()
    
    # Mark the scraped item as scraped in equipment table too
    scrapped_eq = Equipment.query.filter_by(name="Coffee Machine").first()
    scrapped_eq.is_scrapped = True
    db.session.commit()

    print(">>> Maintenance Requests created (8 tickets).")
    print(">>> SEEDING COMPLETE. Run 'python app.py' to start.")