from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, DecimalField
from wtforms.validators import DataRequired, Length

class CreateGroupForm(FlaskForm):
    groupName = StringField("Group name", validators=[DataRequired(), Length(max=50)])
    groupPassword = PasswordField("Group password", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Create")

class JoinGroupForm(FlaskForm):
    groupName = StringField("Group name", validators=[DataRequired(), Length(max=50)])
    groupPassword = PasswordField("Group password", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Join")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    email = EmailField("Email", validators=[DataRequired(), Length(max=70)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Login")

class CreateBillForm(FlaskForm):
    amount = DecimalField("Amount", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired(), Length(max=300)])
    submit = SubmitField("Create bill")
