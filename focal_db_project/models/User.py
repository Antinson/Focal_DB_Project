class User():

    def __init__(self, user_id: int, username: str, password: str, role: str):
        self.id = user_id
        self.username = username
        self.password = password
        self.role = role