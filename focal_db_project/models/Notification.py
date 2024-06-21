from datetime import datetime, timedelta

class Notifications():

    def __init__(self, notification_id: int, message: str, user_id: int, timestamp: datetime):
        self.id = notification_id
        self.message = message
        self.user_id = user_id
        self.timestamp = timestamp