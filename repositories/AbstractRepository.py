import abc
from typing import List

class RepositoryException(Exception):
    def __init__(self, message=None):
        super().__init__(message)

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user(self, user_id: int) -> User:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user_by_username(self, username: str) -> User:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user_list(self) -> List[User]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_cameras_by_user(self, user_id: int) -> List[Camera]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_camera_by_name(self, name: str) -> Camera:
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_camera(self, camera: Camera) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_camera(self, camera: Camera) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete_camera(self, camera: Camera) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_cameras(self) -> List[Camera]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_notification(self, notification: Notification) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete_notification(self, notification_id: int) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_notifications(self) -> List[Notification]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_notification_by_user_id(self, user_id: int) -> Notification:
        raise NotImplementedError
    

