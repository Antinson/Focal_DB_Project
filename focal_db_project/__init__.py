from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from .routes import main, auth
        app.register_blueprint(main.main_bp)
        app.register_blueprint(auth.auth_bp)

        # Repo instance
        from .repositories.SQLAlchemyRepository import SQLAlchemyRepository
        app.repo = SQLAlchemyRepository()
    
    return app