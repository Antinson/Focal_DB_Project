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
    
    user = services.get_user_by_username(username, current_app.repo)
    camera_count = services.get_camera_count_user(user.id, current_app.repo)
    camera_count_broken = services.get_camera_count_broken_user(user.id, current_app.repo)
    camera_count_working = services.get_camera_count_working_user(user.id, current_app.repo)

    return render_template('test_dashboard.html', username=user.username, camera_count=camera_count, camera_count_not_working=camera_count_broken, camera_count_working=camera_count_working) 

@main_bp.route('/addcamera')
@login_required
def add_camera_view():
    return render_template('addcamera.html')

@main_bp.route('/pie/<username>', methods=['GET'])
@login_required
def pie(username):
    user = services.get_user_by_username(username, current_app.repo)
    
    camera_count_broken = services.get_camera_count_broken_user(user.id, current_app.repo)
    camera_count_working = services.get_camera_count_working_user(user.id, current_app.repo)

    data = {
        "labels": ["Working", "Not Working"],
        "values": [camera_count_working, camera_count_broken]
    }
    return jsonify(data)

@main_bp.route('/api/addcamera', methods=['POST'])
@login_required
def add_camera():
    try:
        data = request.json
        camera_name = data.get('cameraid')
        status = data.get('status').lower()

        existing_camera = services.get_camera_by_name(camera_name, current_app.repo)

        if existing_camera:
            if existing_camera.status != status:
                existing_camera.status = status
                services.update_camera(existing_camera, current_app.repo)
                return jsonify({"success": True, "message": "Camera updated", "cameraid": camera_name}), 200
            else:
                return jsonify({"success": False, "message": "Camera already exists", "cameraid": camera_name}), 200
        else:
            new_camera = Camera(name = camera_name, status=status, user_id=current_user.id, storage=current_user.username)
            services.add_camera(new_camera, current_app.repo)
            return jsonify({"success": True, "message": "Camera added", "cameraid": camera_name}), 201
    except Exception as e:
        print('Theres an error')
        print(f'Error: {e}')
        return jsonify({"success": False, "message": str(e)}), 500

# Admin Stuff
@main_bp.route('/addusertodb', methods=['GET'])
def add_user():
    user = User(username='anthony', password='test', role='normal')
    services.add_user(user)
    return jsonify({"message": "User added"})

@main_bp.route('/getcameras', methods=['GET'])
@login_required
def get_cameras():
    cameras = services.get_cameras(current_app.repo)
    return jsonify([{"id": camera.name, "status": camera.status, "user_id": camera.user_id, "storage": camera.storage} for camera in cameras])

@main_bp.route('/getuserlist', methods=['GET'])
@login_required
def get_user_list():
    users = services.get_user_list(current_app.repo)
    return jsonify([{"id": user.id, "username": user.username, "role": user.role} for user in users])

@main_bp.route('/api/checkstocklevels', methods=['GET'])
@login_required
def check_stock_levels():
    user_low_stock = []
    user_list = services.get_user_list(current_app.repo)
    for user in user_list:
        camera_count = services.get_camera_count_broken_user(user.id, current_app.repo)
        if camera_count > 5:
            user_low_stock.append({"username": user.username, "camera_count": camera_count})
    return jsonify(user_low_stock)

@main_bp.route('/api/getnotifications', methods=['GET'])
@login_required
def get_notifications():
    notifications = services.get_notifications(current_app.repo)
    return jsonify([{"id": notification.id, "message": notification.message, "user_id": notification.user_id, "timestamp": notification.timestamp} for notification in notifications])

@main_bp.route('/api/createnotifications', methods=['GET'])
@login_required
def create_notifications():
    user_list = services.get_user_list(current_app.repo)
    for user in user_list:
        camera_count = services.get_camera_count_broken_user(user.id, current_app.repo)
        if camera_count > 5 and not services.get_notification_by_user_id(user.id, current_app.repo):
            notification = Notification(message=f"{user.username} has {camera_count} broken cameras.", user_id=user.id)
            services.add_notification(notification, current_app.repo)
    return jsonify({"message": "Notification created"})

@main_bp.route('/api/deletenotification', methods=['POST'])
@login_required
def delete_notification():
    data = request.json
    notification_id = data.get('id')
    services.delete_notification(notification_id, current_app.repo)
    return jsonify({"message": "Notification deleted"})

