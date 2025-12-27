from.api_routes import api_bp
from .auth_routes import auth_bp
from .equipment_routes import equipment_bp
from .main_routes import main_bp
from .maintenance_routes import maintenance_bp

def register_bp(app):
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(maintenance_bp)