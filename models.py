from flask_login import UserMixin
from configuration import db
from datetime import datetime

"""NOTE TO SELF:
the __tablename__ attribute for each child class of db.Model is set to the class name with snake case
"""


class Users(db.Model, UserMixin):
    id = db.Column("id", db.Integer(), primary_key=True)
    username = db.Column("username", db.String(100), nullable=False, unique=True)
    email = db.Column("email", db.String(100), nullable=False, unique=True)
    password = db.Column("password", db.String(100), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.createdAt = datetime.now()

class Groups(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    name = db.Column("name", db.String(50), unique=True, nullable=False)
    groupPassword = db.Column("groupPassword", db.String(100), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False)

    def __init__(self, name, groupPassword):
        self.name = name
        self.groupPassword = groupPassword
        self.createdAt = datetime.now()

    
    # will also have name, password for the group,

class GroupMembers(db.Model):
    userId = db.Column("userId", db.Integer(), db.ForeignKey("users.id"), nullable=False, primary_key=True)
    groupId = db.Column("groupId", db.Integer(), db.ForeignKey("groups.id"), nullable=False, primary_key=True)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False)

    def __init__(self, userId, groupId):
        self.userId = userId
        self.groupId = groupId
        self.createdAt = datetime.now()


class Bills(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    createdUserId = db.Column("userId", db.Integer(), nullable=False)
    description = db.Column("description", db.String(300))
    createdAt = db.Column("createdAt", db.DateTime, nullable=False)

    def __init__(self, createdUserId, description):
        self.createdUserId = createdUserId
        self.description = description
        self.createdAt = datetime.now()

class Payments(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    userId = db.Column("userId", db.Integer(), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False)
    billId = db.Column("billId", db.Integer(), nullable=False)
    amount = db.Column("amount", db.Numeric(8,2), nullable=False)

    def __init__(self, userId, billId, amount):
        self.userId = userId
        self.billId = billId
        self.amount = amount
        self.createdAt = datetime.now()



class Debtors(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    userId = db.Column("userId", db.Integer(), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False)
    amount = db.Column("amount", db.Numeric(8,2), nullable=False)

    def __init__(self, userId,  amount): # could use the billId here isntead of the amount , but unsure for now
        self.userId = userId
        self.amount = amount
        self.createdAt = datetime.now()




    # will have user name, group member, or maybe user id and group id whatever