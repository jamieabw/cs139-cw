from flask_login import UserMixin
from configuration import db
class User(db.Model, UserMixin):
    id = db.Column("id", db.Integer(), primary_key=True)
    username = db.Column("username", db.String(100), nullable=False, unique=True)
    password = db.Column("password", db.String(100), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password