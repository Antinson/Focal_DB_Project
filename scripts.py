import random
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from focal_db_project import db, create_app
from focal_db_project.models import Camera, CameraScan, User

def random_date(start, end):
    """Generate a random datetime between `start` and `end`."""
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def add_random_timestamps_to_cameras():
    end_date = datetime(2024, 7, 12)
    start_date = end_date - timedelta(days=14)

    cameras = Camera.query.all()

    for camera in cameras:
        num_scans = random.randint(1, 2)  # Number of scans to add per camera
        for _ in range(num_scans):
            random_timestamp = random_date(start_date, end_date)
           
            new_scan = CameraScan(
                camera_name=camera.name,
                user_id=camera.user_id,
                camera_status=camera.status,
                timestamp=random_timestamp
            )
            db.session.add(new_scan)
    
    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        add_random_timestamps_to_cameras()
        print("Random timestamps added successfully.")