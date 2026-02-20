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
    name = db.Column("name", db.String(50), unique=True, nullable=False)
    groupPassword = db.Column("groupPassword", db.String(100), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, name, groupPassword):
        self.name = name
        self.groupPassword = groupPassword

    
    # will also have name, password for the group,

class GroupMembers(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    userId = db.Column("userId", db.Integer(), nullable=False)
    groupId = db.Column("groupId", db.Integer(), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, userId, groupId):
        self.userId = userId
        self.groupId = groupId


class Bills(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    userId = db.Column("userId", db.Integer(), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, userId):
        self.userId = userId

class Payments(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    userId = db.Column("userId", db.Integer(), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False, default=datetime.now())
    billId = db.Column("billId", db.Integer(), nullable=False)
    amount = db.Column("amount", db.Numeric(8,2), nullable=False)

    def __init__(self, userId, billId, amount):
        self.userId = userId
        self.billId = billId
        self.amount = amount


class Debtors(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    userId = db.Column("userId", db.Integer(), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False, default=datetime.now())
    amount = db.Column("amount", db.Numeric(8,2), nullable=False)

    def __init__(self, userId,  amount): # could use the billId here isntead of the amount , but unsure for now
        self.userId = userId
        self.amount = amount




    # will have user name, group member, or maybe user id and group id whatever