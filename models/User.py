class User():

    def __init__(self, user_id: int, username: str, password: str, role: str):
        self.id = user_id
        self.username = username
        self.password = password
        self.role = role




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)