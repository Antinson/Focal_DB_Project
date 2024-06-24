from typing import List
from sqlalchemy.exc import SQLAlchemyError
from .abstract_repo import AbstractRepository, RepositoryException
from ..models import db, User, Camera, Notification

class SQLAlchemyRepository(AbstractRepository):

    def add_user(self, user: User):
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RepositoryException(f"An error occurred while adding the user: {e}")
    
    def get_user(self, user_id: int) -> User:
            try:
                user = User.query.get(user_id)
                if user is None:
                    raise RepositoryException(f"User with ID {user_id} not found.")
                return user
            except SQLAlchemyError as e:
                raise RepositoryException(f"An error occurred while retrieving the user: {e}")
    
    def get_user_by_username(self, username: str) -> User:
        try:
            user = User.query.filter_by(username=username).first()
            if user is None:
                raise RepositoryException(f"User with ID {useername} not found.")
            return user
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while retrieving the user: {e}")

    def get_user_list(self) -> List[User]:
        try:
            users = User.query.all()
            return users
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while retrieving users: {e}")
    
    def get_cameras_by_user(self, user_id: int) -> List[Camera]:
        try:
            cameras = Camera.filter_by(user_id=user_id)
            return cameras
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while retrieving cameras for user: {e}")
    
    def get_camera_by_name(self, name: str) -> Camera:
        try:
            camera = Camera.filter_by(name=name)
            return camera
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while retrieving camera: {e}")

    def add_camera(self, camera: Camera) -> bool:
        try:
            db.session.add(Camera)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RepositoryException(f"An error occurred while adding the camera: {e}")


    def update_camera(self, camera: Camera) -> bool:
        try:
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RepositoryException(f"An error occurred while updating the camera: {e}")

    def delete_camera(self, camera: Camera) -> bool:
        try:
            db.session.delete(camera)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RepositoryException(f"An error occurred while deleting the camera: {e}") 


    def get_cameras(self) -> List[Camera]:
        try:
            cameras = Camera.query.all()
            return cameras
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while retrieving cameras: {e}")


    def add_notification(self, notification: Notification) -> bool:
        try:
            db.session.add(notification)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RepositoryException(f"An error occurred while adding notification: {e}")


    def delete_notification(self, notification_id: int) -> bool:
        try:
            db.session.delete(notification_id)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while deleting notification: {e}")

    def get_notifications(self) -> List[Notification]:
        try:
            notifications = Notification.query.all()
            return notifications
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while getting notifications: {e}")

    def get_notification_by_user_id(self, user_id: int) -> Notification:
        try:
            notification = Notification.filter_by(user_id = user_id).first()
            return notification
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while getting notification: {e}")


    

