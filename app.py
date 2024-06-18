from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///focal_db_project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Dw4F);K^Gnxc|Bek;@MBpjN}c9699|'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Database Stuff
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Camera(db.Model):
    name = db.Column(db.String(120), primary_key=True)
    status = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    storage = db.Column(db.String(120), nullable=False)


# Views
@app.route('/')
@login_required
def home():
    return render_template('home.html', username=current_user.username, role=current_user.role)

@app.route('/user_dashboard/<username>')
@login_required
def user_dashboard(username):
    
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    
    user = User.query.filter_by(username=username).first_or_404()
    camera_count = Camera.query.filter_by(user_id=user.id).count()
    camera_count_not_working = Camera.query.filter_by(user_id=user.id, status='broken').count()
    camera_count_working = Camera.query.filter_by(user_id=user.id, status='working').count()

    return render_template('test_dashboard.html', username=user.username, camera_count=camera_count, camera_count_not_working=camera_count_not_working, camera_count_working=camera_count_working) 

@app.route('/addcamera')
def add_camera_view():
    return render_template('addcamera.html')


# Login Stuff
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid credentials"})
    return render_template('login.html')


@login_manager.unauthorized_handler
def unauthorized():
    # Redirect unauthorized users to the login page
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
 

# API Stuff
@app.route('/pie/<username>', methods=['GET'])
def pie(username):
    user = User.query.filter_by(username=username).first_or_404()
    camera_count_not_working = Camera.query.filter_by(user_id=user.id, status='broken').count()
    camera_count_working = Camera.query.filter_by(user_id=user.id, status='working').count()

    data = {
        "labels": ["Working", "Not Working"],
        "values": [camera_count_working, camera_count_not_working]
    }
    return jsonify(data)

@app.route('/api/addcamera', methods=['POST'])
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

@app.route('/api/addbrokencamera', methods=['POST'])
def add_broken_camera():
    data = request.json
    camera_name = data.get('cameraid')

    new_camera = Camera(name = camera_name, status='broken', user_id=current_user.id, storage=current_user.username)
    db.session.add(new_camera)
    db.session.commit()

    return jsonify({"message": "Camera added", "cameraid": camera_name})

# Admin Stuff
@app.route('/addusertodb', methods=['GET'])
def add_user():
    user = User(username='another', password='test', role='normal')
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User added"})

@app.route('/getcameras', methods=['GET'])
def get_cameras():
    cameras = Camera.query.all()
    return jsonify([{"id": camera.name, "status": camera.status, "user_id": camera.user_id, "storage": camera.storage} for camera in cameras])

@app.route('/getuserlist', methods=['GET'])
def get_user_list():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "role": user.role} for user in users])


@app.route('/api/checkstocklevels', methods=['GET'])
def check_stock_levels():
    user_low_stock = []
    for user in User.query.all():
        camera_count = Camera.query.filter_by(user_id=user.id, status="broken").count()
        if camera_count > 5:
            user_low_stock.append({"username": user.username, "camera_count": camera_count})
    return jsonify(user_low_stock)


if __name__ == '__main__':
    with app.app_context():
            db.create_all()
    app.run(debug=True, host='0.0.0.0', port='8000')
