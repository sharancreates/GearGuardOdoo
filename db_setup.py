from app import create_app
from extension import db 
from models import User, MaintenanceTeams, WorkCentres, Equipment, MaintenanceRequest

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all() 
        print("Database tables created successfully.")