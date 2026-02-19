from flask_login import UserMixin
from configuration import db
from datetime import datetime

class Users(db.Model, UserMixin):
    id = db.Column("id", db.Integer(), primary_key=True)
    username = db.Column("username", db.String(100), nullable=False, unique=True)
    email = db.Column("email", db.String(100), nullable=False, unique=True)
    password = db.Column("password", db.String(100), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False, default=datetime.now())
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Groups(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    # will also have name, password for the group,

class GroupMembers(db.Model):
    ...
    # will have user name, group member, or maybe user id and group id whatever