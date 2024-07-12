from typing import List
from sqlalchemy.exc import SQLAlchemyError
from .AbstractRepository import AbstractRepository, RepositoryException
from ..models import db, User, Camera, Notification, CameraScan
from sqlalchemy.orm import joinedload

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
                raise RepositoryException(f"User with ID {username} not found.")
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
            cameras = Camera.query.filter_by(user_id=user_id).all()
            return cameras
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while retrieving cameras for user: {e}")
    
    def get_camera_by_name(self, name: str) -> Camera:
        try:
            camera = Camera.query.filter_by(name=name).first()
            return camera
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while retrieving camera: {e}")

    def add_camera(self, camera: Camera) -> bool:
        try:
            db.session.add(camera)
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
            notification = self.get_notification_by_id(notification_id)
            db.session.delete(notification)
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
            notification = Notification.query.filter_by(user_id = user_id).first()
            return notification
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while getting notification: {e}")

    def get_notification_by_id(self, notification_id: int) -> Notification:
        try:
            notification = Notification.query.get(notification_id)
            return notification
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while getting notification: {e}")

    def get_camera_count_user(self, user_id: int) -> int:
        try:
            camera_count = Camera.query.filter_by(user_id = user_id).count()
            return camera_count
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while getting camera count: {e}")
    
    def get_camera_count_broken_user(self, user_id: int) -> int:
        try:
            camera_count_broken = Camera.query.filter_by(user_id = user_id, status='broken').count()
            return camera_count_broken
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while getting broken camera count: {e}")

    def get_camera_count_working_user(self, user_id: int) -> int:
        try:
            camera_count_working = Camera.query.filter_by(user_id = user_id, status='working').count()
            return camera_count_working
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while getting working camera count: {e}")
    
      
    def get_camera_by_type(self, camera_type: str) -> List[Camera]:
        try:
            camera_list = Camera.query.filter_by(camera_type = camera_type).all()
            return camera_list
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while getting cameras by type: {e}")
    

    def get_camera_by_type_count_for_user(self, camera_type: str, user_id: int) -> int:
        try:
            camera_count = Camera.query.filter_by(camera_type = camera_type, user_id = user_id).count()
            return camera_count
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while getting cameras by type: {e}")

    def get_camera_list_by_type_for_user(self, camera_type: str, user_id: int) -> List[Camera]:
        try:
            camera_list = Camera.query.filter_by(camera_type = camera_type, user_id = user_id).all()
            return camera_list
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while getting cameras by type: {e}")

    def get_camera_by_user_paginate(self, user_id: int, camera_type: str = None, status: str = None, page: int = 1, per_page: int = 5):
        try:
            query = Camera.query.filter_by(user_id=user_id)
            if camera_type:
                query = query.filter(Camera.camera_type == camera_type)
            if status:
                query = query.filter(Camera.status == status)

            paginated_query = query.paginate(page=page, per_page=per_page, error_out=False)

            return paginated_query
        except SQLAlchemyError as e:
            raise RepositoryException(f"An error occurred while getting cameras by user paginate: {e}")
    
    def get_camera_by_filters(self, user_ids: List[int] = None, countries: List[str] = None, camera_types: List[str] = None, camera_statuses: List[str] = None):
            try:
                query = db.session.query(Camera).options(joinedload(Camera.user))

                if user_ids:
                    query = query.filter(Camera.user_id.in_(user_ids))
                if countries:
                    query = query.join(User).filter(User.country.in_(countries))
                if camera_types:
                    query = query.filter(Camera.camera_type.in_(camera_types))
                if camera_statuses:
                    query = query.filter(Camera.status.in_(camera_statuses))

                cameras = query.all()
                return cameras
            except Exception as e:
                raise RepositoryException(f"An error occurred while getting cameras by filters: {e}")

    
    def get_distinct_users(self, countries: list):
        try:
            query = db.session.query(User.username).distinct()
            if countries:
                query = query.filter(User.country.in_(countries))
            users = [user[0] for user in query.all()]
            return users
        except Exception as e:
            raise RepositoryException(f"An error occurred while getting users by country: {e}")


    
    
    def get_distinct_camera_types(self, countries: list, user_ids: list, camera_statuses: list):
        try:
            query = db.session.query(Camera.camera_type)
            
            if countries:
                query = query.join(User).filter(User.country.in_(countries))
            if user_ids:
                query = query.filter(Camera.user_id.in_(user_ids))
            if camera_statuses:
                query = query.filter(Camera.status.in_(camera_statuses))

            camera_types = query.distinct().all()
            return [camera_type[0] for camera_type in camera_types]
        except Exception as e:
            raise RepositoryException(f"An error occurred while getting camera types: {e}")


 
    def get_distinct_camera_statuses(self, countries: list, user_ids: list, camera_types: list):
        try:
            query = db.session.query(Camera.status)

            if countries:
                query = query.join(User).filter(User.country.in_(countries))
            if user_ids:
                query = query.filter(Camera.user_id.in_(user_ids))
            if camera_types:
                query = query.filter(Camera.camera_type.in_(camera_types))

            found_statuses = set()
            for camera in query.distinct().all():
                found_statuses.add(camera.status)
                if 'broken' in found_statuses and 'working' in found_statuses:
                    break
            
            print(f"Returning statuses: {found_statuses}")  # Debug statement to print found statuses

            return list(found_statuses)
        except Exception as e:
            raise RepositoryException(f"An error occurred while getting camera statuses: {e}")

    
    def get_distinct_countries(self):
        try:
            query = db.session.query(User.country).distinct()
            countries = [country[0] for country in query.all()]
            return countries
        except Exception as e:
            raise RepositoryException(f"An error occurred while getting countries: {e}")

    def get_camera_latest_timestamps_from_list(self, camera_names: List[str]) -> List[str]:
        try:
            # Fetch the latest scans for the provided camera names in a single query
            subquery = (
                db.session.query(
                    CameraScan.camera_name,
                    db.func.max(CameraScan.timestamp).label("latest_timestamp")
                )
                .filter(CameraScan.camera_name.in_(camera_names))
                .group_by(CameraScan.camera_name)
                .subquery()
            )

            latest_scans = (
                db.session.query(CameraScan.timestamp, CameraScan.camera_status)
                .join(subquery, db.and_(
                    CameraScan.camera_name == subquery.c.camera_name,
                    CameraScan.timestamp == subquery.c.latest_timestamp
                ))
                .all()
            )

            # Process the results
            result = [(scan.timestamp, scan.camera_status) for scan in latest_scans]
            return result
        except Exception as e:
            raise RepositoryException(f"An error occurred while getting latest timestamps: {e}")


    def get_camera_timestamps_single(self, camera_name: str) -> List[str]:
        try:
            scans = db.session.query(CameraScan).filter_by(camera_name=camera_name).order_by(CameraScan.timestamp.desc()).all()
            return [scan.timestamp for scan in scans]
        except Exception as e:
            raise RepositoryException(f"An error occurred while getting timestamps for camera {camera_name}: {e}")