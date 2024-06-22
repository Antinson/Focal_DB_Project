from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from ..models import User
from .. import login_manager

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
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
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
 

@login_manager.unauthorized_handler
def unauthorized():
    # Redirect unauthorized users to the login page
    return redirect(url_for('auth.login'))