from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app