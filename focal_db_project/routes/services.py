from typing import List, Iterable
from focal_db_project.repositories import AbstractRepository
from focal_db_project.models import User, Camera, Notification

class NameNotUniqueException(Exception):
    pass

class UnknownUserException(Exception):
    pass

class AuthenticationException(Exception):
    pass


def add_user(user: User, repo: AbstractRepository):
    return repo.add_user(user)

def get_user(user_id: int, repo: AbstractRepository):
    return repo.get_user(user_id)

def get_user_by_username(username: str, repo: AbstractRepository):
    return repo.get_user_by_username(username)

def get_user_list(repo: AbstractRepository):
    return repo.get_user_list()

def get_cameras_by_user(user_id: int, repo: AbstractRepository):
    return repo.get_cameras_by_user(user_id)

def get_camera_by_name(name: str, repo: AbstractRepository):
    return repo.get_camera_by_name(name)

def add_camera(camera: Camera, repo: AbstractRepository):
    return repo.add_camera(camera)

def update_camera(camera: Camera, repo: AbstractRepository):
    return repo.update_camera(camera)

def delete_camera(camera: Camera, repo: AbstractRepository):
    return repo.delete_camera(camera)

def add_notification(notification: Notification, repo: AbstractRepository):
    return repo.add_notification(notification)

def delete_notification(notification_id: int, repo: AbstractRepository):
    return repo.delete_notification(notification_id)

def get_notifications(repo: AbstractRepository):
    return repo.get_notifications()

def get_notification_by_user_id(user_id: int, repo: AbstractRepository):
    return repo.get_notification_by_user_id(user_id)






