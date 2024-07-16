from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from ..models import User
from .. import login_manager
from .. import db
import focal_db_project.routes.services as services
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user = services.get_user_by_username(username, current_app.repo)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid credentials"})
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
 

@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register_user():
    if request.method == 'POST':
        try:
            data = request.json
            username = data.get('username').lower()
            password = data.get('password')
            role = data.get('role')
            country = data.get('country')
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            user = User(username=username, password=hashed_password, role=role, country=country)
            services.add_user(user, current_app.repo)
            return jsonify({"message": "Creation successful"})
        except Exception as e:
            print(e)
            return jsonify({"message": "Something went wrong"})
    return render_template('register.html', role=current_user.role)

@login_manager.unauthorized_handler
def unauthorized():
    # Redirect unauthorized users to the login page
    return redirect(url_for('auth.login'))