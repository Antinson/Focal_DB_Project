from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from .routes import main, auth
        app.register_blueprint(main.main_bp)
        app.register_blueprint(auth.auth_bp)
    
    return app