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
    creatorId = db.Column("creatorId", db.ForeignKey("users.id"), nullable=False)
    groupId = db.Column("groupId", db.ForeignKey("groups.id"), nullable=False)
    description = db.Column("description", db.String(250))
    total = db.Column("total", db.Numeric(8,2), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False)
    group = db.relationship("Groups", foreign_keys=[groupId])
    creator = db.relationship("Users", foreign_keys=[creatorId])

    def __init__(self, creatorId, groupId, description, total):
        self.creatorId = creatorId
        self.groupId = groupId
        self.description = description
        self.total = total
        self.createdAt = datetime.now()

class Payments(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    billId = db.Column("billId", db.ForeignKey("bills.id"), nullable=False)
    payerId = db.Column("payerId", db.ForeignKey("users.id"), nullable=False)
    payeeId = db.Column("payeeId", db.ForeignKey("users.id"), nullable=False)
    amount = db.Column("amount", db.Numeric(8,2), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False)
    evidence = db.Column("evidence", db.LargeBinary, nullable=True) # temp
    status = db.Column("status", db.String(15)) # pending, acknowledged, rejected
    bill = db.relationship("Bills", foreign_keys=[billId])
    user = db.relationship("Users", foreign_keys=[payerId])

    def __init__(self, billId, payerId, payeeId, amount, evidence):
        self.billId = billId
        self.payerId = payerId
        self.payeeId = payeeId
        self.amount = amount
        self.evidence = evidence
        self.status = "pending"
        self.createdAt = datetime.now()



class Debtors(db.Model):
    billId = db.Column("billId", db.ForeignKey("bills.id"), primary_key=True)
    userId = db.Column("userId", db.ForeignKey("users.id"), primary_key=True)
    proportion = db.Column("proportion", db.Numeric(3, 2))
    owed = db.Column("owed", db.Numeric(8,2))
    createdAt = db.Column("createdAt", db.DateTime, nullable=False)
    bill = db.relationship("Bills", foreign_keys=[billId])
    user = db.relationship("Users", foreign_keys=[userId])
    status = db.Column("status", db.String(8))  # paid/unpaid

    def __init__(self, billId, userId, proportion, owed):
        self.billId = billId
        self.userId = userId
        self.proportion = proportion
        self.owed = owed
        self.status = "unpaid"
        self.createdAt = datetime.now()

"""
notifcation types will be a payment noti, settlement/rejection noti, editing/creating bill noti,
the emails will be have the same template, with just things like type and creator filled out

i think this works, probably not though
"""
class Notifications(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    groupId = db.Column("groupId", db.ForeignKey("groups.id"))
    userId = db.Column("userId", db.ForeignKey("users.id"))
    creatorId = db.Column("creatorId", db.ForeignKey("users.id"))
    type = db.Column("type", db.String(40))
    group = db.relationship("Groups", foreign_keys=[groupId])
    creator = db.relationship("Users", foreign_keys=[creatorId])
    createdAt = db.Column("createdAt", db.DateTime, nullable=False)

    def __init__(self, groupId, userId, creatorId, type):
        self.groupId = groupId
        self.userId = userId
        self.creatorId = creatorId
        self.type = type
        self.createdAt = datetime.now()

"""
types: "create bill", "edit bill", "payment acknowledged", "payment rejected", "bill payment"
"""

class BillLog(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    userId = db.Column("userId", db.ForeignKey("users.id"))
    billId = db.Column("billId", db.ForeignKey("bills.id"))
    information = db.Column("information", db.String(300))
    createdAt = db.Column("createdAt", db.DateTime, nullable=False)
    user = db.relationship("Users", foreign_keys=[userId])
    bill = db.relationship("Bills", foreign_keys=[billId])

    def __init__(self, userId, billId, information):
        self.userId = userId
        self.information = information
        self.billId = billId
        self.createdAt = datetime.now()
    """
    bill log for creating, payment, editing
    """

class LoginAttemptLogs(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    userId = db.Column("userId", db.ForeignKey("users.id"))
    information = db.Column("information", db.String(300))
    successful = db.Column("successful", db.Boolean(), nullable=False)
    createdAt = db.Column("createdAt", db.DateTime, nullable=False)
    user = db.relationship("Users", foreign_keys=[userId])


    def __init__(self, userId, information, successful):
        self.userId = userId
        self.information = information
        self.successful = successful
        self.createdAt = datetime.now()

"""
events to log: created account, login failure, login success, !password change, !email change, !recovery attempt
! - extras
"""



    # will have user name, group member, or maybe user id and group id whatever