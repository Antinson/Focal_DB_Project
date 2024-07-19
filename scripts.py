import random
from datetime import datetime, timedelta
from focal_db_project import db, create_app
from focal_db_project.models import Camera, CameraScan, User
from werkzeug.security import generate_password_hash, check_password_hash

def random_date(start, end):
    """Generate a random datetime between `start` and `end`."""
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def add_random_timestamps_to_cameras(username):
    end_date = datetime(2024, 7, 19)
    start_date = end_date - timedelta(days=14)

    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"User {username} not found.")
        return

    cameras = Camera.query.filter_by(user_id=user.id).all()
    if not cameras:
        print(f"No cameras found for user {username}.")
        return

    for camera in cameras:
        num_scans = random.randint(1, 2)  # Number of scans to add per camera
        for _ in range(num_scans):
            random_timestamp = random_date(start_date, end_date)
           
            new_scan = CameraScan(
                camera_name=camera.name,
                user_id=camera.user_id,
                camera_status=random_status(),  # Use random_status() here
                timestamp=random_timestamp
            )
            db.session.add(new_scan)
    
    db.session.commit()
    print(f"Random timestamps added to cameras for user {username} successfully.")

def update_user():
    pass


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        update_user()
