from flask import Flask, render_template
from config import Config
from extension import db
from flask_login import LoginManager
from routes import register_bp
from models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        return render_template('landing.html')
    
    register_bp(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug = True)
