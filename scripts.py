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

def add_cameras_to_test_accounts():
    # Read camera MAC addresses and add to the test accounts
    with open('nz_mac_address.txt', 'r') as file:
        nz_mac_addresses = file.read().splitlines()
    
    with open('au_mac_address.txt', 'r') as file:
        au_mac_addresses = file.read().splitlines()

    nz_user = User.query.filter_by(username='nz_user_test').first()
    au_user = User.query.filter_by(username='au_user_test').first()

    if not nz_user or not au_user:
        print("One or both test users not found.")
        return

    for mac_address in nz_mac_addresses:
        camera = Camera(name=mac_address, user_id=nz_user.id, status=random_status(), storage='nz_user_test', camera_type=random_camera_type())
        db.session.add(camera)
    
    for mac_address in au_mac_addresses:
        camera = Camera(name=mac_address, user_id=au_user.id, status=random_status(), storage='au_user_test', camera_type=random_camera_type())
        db.session.add(camera)

    db.session.commit()
    print("Cameras added to test accounts successfully.")

def random_status():
    return random.choice(['working', 'broken'])

def random_camera_type():
    camera_types = ['FM-21', 'FM-88', 'SE-88', 'FM-62', 'FM-40']
    return random.choice(camera_types)

def update_camera_types():
    app = create_app()
    with app.app_context():
        # Query cameras with null type
        cameras = Camera.query.filter(Camera.camera_type.is_(None)).all()

        # Update camera types
        for camera in cameras:
            camera.type = random_camera_type()
            db.session.add(camera)
        
        # Commit changes
        db.session.commit()
        print(f"Updated {len(cameras)} cameras with random types.")


if __name__ == "__main__":
    update_camera_types()
