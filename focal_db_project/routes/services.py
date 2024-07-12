from typing import List, Iterable
from focal_db_project.repositories import AbstractRepository
from focal_db_project.models import User, Camera, Notification, CameraScan

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
    username = username.lower()
    return repo.get_user_by_username(username)

def get_user_list(repo: AbstractRepository):
    return repo.get_user_list()

def get_cameras_by_user(user_id: int, repo: AbstractRepository):
    return repo.get_cameras_by_user(user_id)

def get_cameras(repo: AbstractRepository):
    return repo.get_cameras()

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

def get_notification_by_id(notification_id: int, repo: AbstractRepository):
    return repo.get_notification_by_id(notification_id)

def get_notification_by_user_id(user_id: int, repo: AbstractRepository):
    return repo.get_notification_by_user_id(user_id)

def get_camera_count_user(user_id: int, repo: AbstractRepository) -> int:
    return repo.get_camera_count_user(user_id)

def get_camera_count_broken_user(user_id: int, repo: AbstractRepository) -> int:
    return repo.get_camera_count_broken_user(user_id)

def get_camera_count_working_user(user_id: int, repo: AbstractRepository) -> int:
    return repo.get_camera_count_working_user(user_id)

def get_camera_by_type(camera_type: str, repo: AbstractRepository) -> List[Camera]:
    return repo.get_camera_by_type(camera_type)

def get_camera_by_type_count_for_user(camera_type: str, user_id: int, repo: AbstractRepository) -> int:
    return repo.get_camera_by_type_count_for_user(camera_type, user_id)

def get_camera_list_by_type_for_user(camera_type: str, user_id: int, repo: AbstractRepository) -> List[Camera]:
    return repo.get_camera_list_by_type_for_user(camera_type, user_id)

def get_all_type_counts_for_user(user_id, repo: AbstractRepository):
    camera_list = get_cameras_by_user(user_id, repo)
    camera_data = {}
    for camera in camera_list:
        if camera.camera_type not in camera_data:
            camera_data[camera.camera_type] = get_camera_by_type_count_for_user(camera.camera_type, user_id, repo)
    return camera_data


def get_camera_by_user_paginate(user_id: int, repo: AbstractRepository, camera_type: str = None, status: str = None, page: int = 1, per_page: int = 5):
    return repo.get_camera_by_user_paginate(user_id, camera_type, status, page, per_page)


def get_camera_by_filters(repo: AbstractRepository, user_ids: List[int] = None, countries: List[str] = None, camera_types: List[str] = None, camera_statuses: List[str] = None):
    return repo.get_camera_by_filters(user_ids, countries, camera_types, camera_statuses)

def get_distinct_users(countries: List[str], repo: AbstractRepository) -> List[str]:
    return repo.get_distinct_users(countries)

def get_distinct_camera_types(countries: List[str], user_ids: List[int], camera_statuses: List[str], repo: AbstractRepository) -> List[str]:
    return repo.get_distinct_camera_types(countries, user_ids, camera_statuses)

def get_distinct_camera_statuses(countries: List[str], user_ids: List[int], camera_types: List[str], repo: AbstractRepository) -> List[str]:
    return repo.get_distinct_camera_statuses(countries, user_ids, camera_types)

def get_distinct_countries(repo: AbstractRepository) -> List[str]:
    return repo.get_distinct_countries()

def get_camera_latest_timestamps_from_list(camera_names: List[str], repo: AbstractRepository) -> List[str]:
    return repo.get_camera_latest_timestamps_from_list(camera_names)

def get_camera_timestamps_single(camera_name: str, repo: AbstractRepository) -> List[str]:
    return repo.get_camera_timestamps_single(camera_name)