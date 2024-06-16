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
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    storage = db.Column(db.String(120), nullable=False)

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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/addcamera')
def add_camera_view():
    return render_template('addcamera.html')

@app.route('/addbrokencamera')
def add_broken_camera_view():
    return render_template('addbrokencamera.html')

@app.route('/editcamera')
def editcamera():
    return render_template('editcamera.html')


@app.route('/api/addcamera', methods=['POST'])
def add_camera():
    data = request.json
    data['status'] = 'working'
    camera_id = data.get('cameraid')
    # Add your logic to handle the camera ID (e.g., save it to the database)
    return jsonify({"message": "Camera added", "cameraid": camera_id})

@app.route('/api/addbrokencamera', methods=['POST'])
def add_broken_camera():
    data = request.json
    camera_id = data.get('cameraid')
    # Add your logic to handle the camera ID (e.g., save it to the database)
    new_camera = Camera(status='broken', user_id=current_user.id, storage=current_user.username)
    db.session.add(new_camera)
    db.session.commit()

    return jsonify({"message": "Camera added", "cameraid": camera_id})

@app.route('/addusertodb', methods=['GET'])
def add_user():
    user = User(username='ant', password='ant', role='normal')
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User added"})

@app.route('/getcameras', methods=['GET'])
def get_cameras():
    cameras = Camera.query.all()
    return jsonify([{"id": camera.id, "status": camera.status, "user_id": camera.user_id, "storage": camera.storage} for camera in cameras])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
