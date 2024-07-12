from datetime import datetime
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    cameras = db.relationship('Camera', back_populates='user')
    scans = db.relationship('CameraScan', back_populates='user', cascade='all, delete-orphan')

class Camera(db.Model):
    name = db.Column(db.String(120), primary_key=True)
    status = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    storage = db.Column(db.String(120), nullable=False)
    camera_type = db.Column(db.String(6), nullable=True)

    user = db.relationship('User', back_populates='cameras')
    scans = db.relationship('CameraScan', back_populates='camera', cascade='all, delete-orphan')

class CameraScan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_name = db.Column(db.String(120), db.ForeignKey('camera.name'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    camera_status = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    camera = db.relationship('Camera', back_populates='scans')
    user = db.relationship('User', back_populates='scans')


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)