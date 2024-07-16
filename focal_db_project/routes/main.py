from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint, current_app, send_file, make_response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from ..models import User, Camera, Notification
from .. import db
import focal_db_project.routes.services as services
import pandas as pd
import io
import openpyxl


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def home():
    return render_template('new_home.html', username=current_user.username, role=current_user.role)

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

@main_bp.route('/api/get-camera-counts-by-type/<username>')
@login_required
def get_camera_counts_by_type(username):
    user = services.get_user_by_username(username, current_app.repo)
    camera_counts_by_type = services.get_all_type_counts_for_user(user.id, current_app.repo)
    
    json_ready_data = {("None" if k is None else k): v for k, v in camera_counts_by_type.items()}

    response = jsonify(json_ready_data)
    return response

@main_bp.route('/addcamera')
@login_required
def add_camera_view():
    return render_template('addcamera.html', role=current_user.role)

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
        camera_type = data.get('camera_type').upper()

        existing_camera = services.get_camera_by_name(camera_name, current_app.repo)

        if existing_camera:
            if existing_camera.status != status or existing_camera.camera_type != camera_type:
                existing_camera.status = status
                existing_camera.camera_type = camera_type
                services.update_camera(existing_camera, current_app.repo)
                return jsonify({"success": True, "message": "Camera updated", "cameraid": camera_name}), 200
            else:
                return jsonify({"success": False, "message": "Camera already exists", "cameraid": camera_name}), 200
        else:
            new_camera = Camera(name = camera_name, status=status, user_id=current_user.id, storage=current_user.username, camera_type = camera_type)
            services.add_camera(new_camera, current_app.repo)
            return jsonify({"success": True, "message": "Camera added", "cameraid": camera_name}), 201
    except Exception as e:
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

@main_bp.route('/api/download-usertable', methods=['POST'])
@login_required
def download_user_table():
    data = request.json
    user = services.get_user_by_username(data.get('user'), current_app.repo)
    users_cameras = services.get_cameras_by_user(user.id, current_app.repo)
    filetype = data.get('filetype', 'json').lower()
    
    camera_data = [{
        'camera_name': camera.name,
        'camera_status': camera.status,
        'camera_user_id': camera.user_id,
        'camera_storage': camera.storage,
        'camera_type': camera.camera_type
    } for camera in users_cameras]

    df = pd.DataFrame(camera_data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if (filetype == "excel"):
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        
        output.seek(0)

        return send_file(output,
                        download_name=f"{user.username}-{timestamp}.xlsx",
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        response = make_response(jsonify(camera_data))
        response.headers["Content-Disposition"] = f"attachment; filename={user.username}-{timestamp}.json"
        response.headers["Content-Type"] = "application/json"
        return response


@main_bp.route('/api/get-camera-user/<username>', methods=['GET'])
@login_required
def get_camera_user(username):
    try:
        username = username.lower()
        user = services.get_user_by_username(username, current_app.repo)

        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))

        # Fetch filtered data if camera_type or status are provided
        camera_type = request.args.get('camera_type')
        status = request.args.get('status')

        users_cameras = services.get_camera_by_user_paginate(user.id, current_app.repo, camera_type, status, page, per_page)

        camera_data = [{
            'camera_name': camera.name,
            'camera_status': camera.status,
            'camera_user_id': camera.user_id,
            'camera_storage': camera.storage,
            'camera_type': camera.camera_type
        } for camera in users_cameras.items]

        return jsonify({
            'data': camera_data,
            'total': users_cameras.total,
            'page': users_cameras.page,
            'per_page': users_cameras.per_page
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching camera data for user {username}: {e}")
        return jsonify({'error': 'Something went wrong!'}), 500



@main_bp.route('/user-test/<username>', methods=['GET'])
@login_required
def user_test_page(username):
    return render_template('my_cameras.html', user=username, role=current_user.role)


@main_bp.route('/editcamera/<camera>', methods=['GET'])
@login_required
def edit_camera_test(camera):
    return render_template('editcamera.html', camera=camera, role=current_user.role)


@main_bp.route('/api/updatecamera', methods=['POST'])
@login_required
def update_camera():
    try:
        new_camera_values = request.json
        camera_name = new_camera_values.get('camera_name')
        camera = services.get_camera_by_name(camera_name, current_app.repo)

        if (camera.user_id == current_user.id or current_user.role == 'admin'):
            camera.status = new_camera_values.get('camera_status')
            camera.camera_type = new_camera_values.get('camera_type')
            services.update_camera(camera, current_app.repo)
            print(camera.camera_type)
            return jsonify({'message': 'update successful'})
        return jsonify({'message': 'update un-successful'})
    except Exception as e:
        return jsonify({'message': 'Something went very wrong'})

@main_bp.route('/camera-test', methods=['GET'])
@login_required
def camera_testing_update():
    return render_template('editpage.html', role=current_user.role)

@main_bp.route('/api/getspecificcamera', methods=['POST'])
@login_required
def get_specific_camera():
    try:
        data = request.json
        camera_name = data.get('camera_name')
        camera = services.get_camera_by_name(camera_name, current_app.repo)

        camera_data = {
            'camera_name': camera.name,
            'camera_status': camera.status,
            'camera_type': camera.camera_type
        }

        return jsonify(camera_data)

    except Exception as e:
        return jsonify({'message': 'Something went very wrong'})

@main_bp.route('/api/deletecamera', methods=['POST'])
@login_required
def delete_camera():
    try:
        data = request.json
        camera_name = data.get('camera_name')
        camera_to_delete = services.get_camera_by_name(camera_name, current_app.repo)
        services.delete_camera(camera_to_delete, current_app.repo)
        return jsonify({'message': 'Deletion Successful'})
    except Exception as e:
        return jsonify({'message': 'Something went wrong'})


@main_bp.route('/test')
@login_required
def test():
    return render_template('new_home.html', role=current_user.role)


@main_bp.route('/api/get-cameras-dash', methods=['POST'])
@login_required
def get_cameras_dash():
    # Get filter values from request
    data = request.json

    if current_user.role != 'admin':
        countries = [current_user.country]
        users = [current_user.username]
    else:
        countries = data.get('country', [])
        users = data.get('user', [])
    
    camera_types = data.get('cameraType', [])
    camera_statuses = data.get('cameraStatus', [])

    user_filters = []
    if users:
        for user in users:
            user_obj = services.get_user_by_username(user, current_app.repo)
            if user_obj:
                user_filters.append(user_obj.id)

    filtered_data = services.get_camera_by_filters(
        repo=current_app.repo, 
        user_ids=user_filters, 
        countries=countries, 
        camera_types=camera_types, 
        camera_statuses=camera_statuses
    )

    total = len(filtered_data)
    broken = len([camera for camera in filtered_data if camera.status == 'broken'])
    working = total - broken

    camera_data = [{
        'camera_name': camera.name,
        'camera_status': camera.status,
        'camera_user_id': camera.user_id,
        'camera_storage': camera.storage,
        'camera_type': camera.camera_type,
        'camera_country': camera.user.country,
    } for camera in filtered_data]

    counts = {
        'total': total,
        'broken': broken,
        'working': working
    }

    response = {
        'cameras': camera_data,
        'counts': counts
    }

    return jsonify(response)


@main_bp.route('/api/get-filtered-options', methods=['POST'])
@login_required
def get_filtered_options():
    data = request.json

    if current_user.role != 'admin':
        countries = [current_user.country]
        users = [current_user.username]
    else:
        countries = data.get('country', [])
        users = data.get('user', [])

    camera_types = data.get('cameraType', [])
    camera_statuses = data.get('cameraStatus', [])


    user_filters = []
    if users:
        for user in users:
            user_obj = services.get_user_by_username(user, current_app.repo)
            if user_obj:
                user_filters.append(user_obj.id)

    distinct_countries = services.get_distinct_countries(repo=current_app.repo)
    distinct_users = services.get_distinct_users(countries, current_app.repo)
    distinct_camera_types = services.get_distinct_camera_types(countries, user_filters, camera_statuses, current_app.repo)
    distinct_camera_statuses = services.get_distinct_camera_statuses(countries, user_filters, camera_types, current_app.repo)

    filter_options = {
        'countries': distinct_countries,
        'users': distinct_users,
        'camera_types': distinct_camera_types,
        'camera_statuses': distinct_camera_statuses
    }

    return jsonify(filter_options)


@main_bp.route('/api/get-timestamps', methods=['POST'])
@login_required
def get_timestamps_from_list():
    
    data = request.json
    camera_names = data.get('camera_names', [])

    camera_timestamps = services.get_camera_latest_timestamps_from_list(camera_names, current_app.repo)
    response_data = [{'timestamp': ts.isoformat(), 'status': status} for ts, status in camera_timestamps]

    return jsonify(response_data)

@main_bp.route('/api/download-table', methods=['POST'])
@login_required
def download_table():
    print("Download table endpoint reached")
    data = request.json

    if current_user.role != 'admin':
        countries = [current_user.country]
        users = [current_user.username]
    else:
        countries = data.get('country', [])
        users = data.get('user', [])
    
    camera_types = data.get('cameraType', [])
    camera_statuses = data.get('cameraStatus', [])

    user_filters = []
    if users:
        for user in users:
            user_obj = services.get_user_by_username(user, current_app.repo)
            if user_obj:
                user_filters.append(user_obj.id)

    filtered_data = services.get_camera_by_filters(
        repo=current_app.repo, 
        user_ids=user_filters, 
        countries=countries, 
        camera_types=camera_types, 
        camera_statuses=camera_statuses
    )

    camera_data = [{
        'camera_name': camera.name,
        'camera_status': camera.status,
        'camera_user_id': camera.user_id,
        'camera_storage': camera.storage,
        'camera_type': camera.camera_type,
        'camera_country': camera.user.country,
    } for camera in filtered_data]

    print("Filtered camera data:", camera_data)

    try:
        df = pd.DataFrame(camera_data)
    except Exception as e:
        print("Error creating DataFrame:", e)
        return jsonify({"error": "Error creating DataFrame"}), 500
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = io.BytesIO()

    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
    except Exception as e:
        print("Error writing Excel file:", e)
        return jsonify({"error": "Error writing Excel file"}), 500
    
    
    output.seek(0)

    try:
        return send_file(output,
                        download_name=f"focal_cameras_{timestamp}.xlsx",
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        print("Error sending file:", e)
        return jsonify({"error": "Error sending file"}), 500