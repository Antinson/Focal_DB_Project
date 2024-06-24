from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint, current_app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from ..models import User, Camera, Notification
from .. import db
import focal_db_project.routes.services as services


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def home():
    return render_template('home.html', username=current_user.username, role=current_user.role)

@main_bp.route('/user_dashboard/<username>')
@login_required
def user_dashboard(username):
    
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    
    user = services.get_user_by_username(username, repo.current_app)
    cameras = services.get_cameras_by_user(user.id, repo.current_app)

    camera_count = len(cameras)

    camera_count = Camera.query.filter_by(user_id=user.id).count()
    camera_count_not_working = Camera.query.filter_by(user_id=user.id, status='broken').count()
    camera_count_working = Camera.query.filter_by(user_id=user.id, status='working').count()

    return render_template('test_dashboard.html', username=user.username, camera_count=camera_count, camera_count_not_working=camera_count_not_working, camera_count_working=camera_count_working) 

@main_bp.route('/addcamera')
@login_required
def add_camera_view():
    return render_template('addcamera.html')

@main_bp.route('/pie/<username>', methods=['GET'])
@login_required
def pie(username):
    user = User.query.filter_by(username=username).first_or_404()
    camera_count_not_working = Camera.query.filter_by(user_id=user.id, status='broken').count()
    camera_count_working = Camera.query.filter_by(user_id=user.id, status='working').count()

    data = {
        "labels": ["Working", "Not Working"],
        "values": [camera_count_working, camera_count_not_working]
    }
    return jsonify(data)

@main_bp.route('/api/addcamera', methods=['POST'])
@login_required
def add_camera():
    data = request.json
    print(data)
    camera_name = data.get('cameraid')
    status = data.get('status').lower()

    existing_camera = Camera.query.filter_by(name=camera_name).first()
    if existing_camera:
        if existing_camera.status != status:
            existing_camera.status = status
            db.session.commit()
            return jsonify({"message": "Camera updated", "cameraid": camera_name})
        else:
            return jsonify({"message": "Camera already exists", "cameraid": camera_name})
    else:
        new_camera = Camera(name = camera_name, status=status, user_id=current_user.id, storage=current_user.username)
        db.session.add(new_camera)
        db.session.commit()
        return jsonify({"message": "Camera added", "cameraid": camera_name})

# Admin Stuff
@main_bp.route('/addusertodb', methods=['GET'])
def add_user():
    user = User(username='anthony', password='test', role='normal')
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User added"})

@main_bp.route('/getcameras', methods=['GET'])
@login_required
def get_cameras():
    cameras = Camera.query.all()
    return jsonify([{"id": camera.name, "status": camera.status, "user_id": camera.user_id, "storage": camera.storage} for camera in cameras])

@main_bp.route('/getuserlist', methods=['GET'])
@login_required
def get_user_list():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "role": user.role} for user in users])

@main_bp.route('/api/checkstocklevels', methods=['GET'])
@login_required
def check_stock_levels():
    user_low_stock = []
    for user in User.query.all():
        camera_count = Camera.query.filter_by(user_id=user.id, status="broken").count()
        if camera_count > 5:
            user_low_stock.append({"username": user.username, "camera_count": camera_count})
    return jsonify(user_low_stock)

@main_bp.route('/api/getnotifications', methods=['GET'])
@login_required
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([{"id": notification.id, "message": notification.message, "user_id": notification.user_id, "timestamp": notification.timestamp} for notification in notifications])

@main_bp.route('/api/createnotifications', methods=['GET'])
@login_required
def create_notifications():
    for user in User.query.all():
        camera_count = Camera.query.filter_by(user_id=user.id, status="broken").count()
        if camera_count > 5 and not Notification.query.filter_by(user_id=user.id).first():
            notification = Notification(message=f"{user.username} has {camera_count} broken cameras.", user_id=user.id)
            db.session.add(notification)
            db.session.commit()
    return jsonify({"message": "Notification created"})

@main_bp.route('/api/deletenotification', methods=['POST'])
@login_required
def delete_notification():
    data = request.json
    notification_id = data.get('id')
    notification = Notification.query.filter_by(id=notification_id).first()
    db.session.delete(notification)
    db.session.commit()
    return jsonify({"message": "Notification deleted"})

