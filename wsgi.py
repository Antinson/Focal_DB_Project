from focal_db_project import create_app, db
from werkzeug.security import generate_password_hash
from focal_db_project.models import User

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

