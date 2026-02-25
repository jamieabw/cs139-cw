from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, DecimalField, FileField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import file_required, file_allowed
from models import Groups, Users

class CreateGroupForm(FlaskForm):
    groupName = StringField("Group name", validators=[DataRequired(), Length(max=50)])
    groupPassword = PasswordField("Group password", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Create")

    def validate_groupName(self, groupName):
        nameToCheck = Groups.query.filter_by(name=groupName.data).first()
        if nameToCheck:
            raise ValidationError("Group name is already taken.")

class JoinGroupForm(FlaskForm):
    groupName = StringField("Group name", validators=[DataRequired(), Length(max=50)])
    groupPassword = PasswordField("Group password", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Join")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    email = EmailField("Email", validators=[DataRequired(), Length(max=70)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Register")

    def validate_username(self, username):
        nameToCheck = Users.query.filter_by(username=username.data).first()
        if nameToCheck:
            raise ValidationError("Username is already taken.")
        

    def validate_email(self, email):
        emailToCheck = Users.query.filter_by(email=email.data).first()
        if emailToCheck:
            raise ValidationError("Email is already taken.")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Login")

    def validate_username(self, username):
        nameToCheck = Users.query.filter_by(username=username.data).first()
        if not nameToCheck:
            raise ValidationError("User credentials do not match.")

class CreateBillForm(FlaskForm):
    amount = DecimalField("Amount", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired(), Length(max=300)])
    submit = SubmitField("Create bill")

class SettleDebtForm(FlaskForm):
    billId = HiddenField(render_kw={"id": "billId"})
    evidence = FileField("Evidence", validators=[file_required(), file_allowed({"jpg", "png"}, "Evidence must be an image.")])
    submit = SubmitField("Send settle request")

class updateAccountDetailsForm(FlaskForm):
    ... # form for updating account details
