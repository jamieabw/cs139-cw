from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, EmailField, PasswordField, DecimalField, FileField, HiddenField, DecimalRangeField, FieldList, FormField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange, EqualTo
from flask_wtf.file import file_required, file_allowed
from models import Groups, Users
from flask_login import current_user

class CreateGroupForm(FlaskForm):
    groupName = StringField("Group name", validators=[DataRequired(), Length(max=50)])
    groupPassword = PasswordField("Group password", validators=[DataRequired(), Length(max=50)])
    confirmGroupPassword = PasswordField("Confirm group password", validators=[DataRequired(), Length(max=50), EqualTo("groupPassword", "Passwords must match.")])

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
    confirmPassword = PasswordField("Confirm password", validators=[DataRequired(), Length(max=50), EqualTo("password", "Passwords must match.")])
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
        

class SettleDebtForm(FlaskForm):
    billId = HiddenField(render_kw={"id": "billId"})
    evidence = FileField("Evidence", validators=[file_required(), file_allowed({"jpg", "png"}, "Evidence must be an image.")])
    submit = SubmitField("Send settle request")

class ProportionSharingForm(Form): # inhreits Form instead to fix below issue
    # seems like this is causing an error as the values arent actually get passed
    memberId = HiddenField(validators=[DataRequired()])
    memberName = HiddenField(validators=[DataRequired()])
    proportion = DecimalRangeField(validators=[NumberRange(min=0, max=100)], render_kw={"min": 0, "max": 100, "step": 0.01})

class CreateBillForm(FlaskForm):
    total = DecimalField("Total", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired(), Length(max=300)])
    proportions = FieldList(FormField(ProportionSharingForm), min_entries=0)
    submit = SubmitField("Create bill")

    def validate_proportions(self, proportions):
        total = 0
        for entry in proportions.entries:
            total += float(entry.form.proportion.data)
        if total < 99.9 or total > 100.1: # small error margin for recuring decimals like 1/3 etc
            raise ValidationError("Total must be ~100%.")
        
class updateAccountDetailsForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    email = EmailField("Email", validators=[DataRequired(), Length(max=70)])
    submit = SubmitField("Update details")

    def validate_username(self, username):
        nameToCheck = Users.query.filter_by(username=username.data).first()
        if nameToCheck and nameToCheck.username != current_user.username:
            raise ValidationError("Username is already taken.")
        
    def validate_email(self, email):
        emailToCheck = Users.query.filter_by(email=email.data).first()
        if emailToCheck and emailToCheck.email != current_user.email:
            raise ValidationError("Email is already taken.")

class updatePasswordForm(FlaskForm):
    currentPassword = PasswordField("Current password", validators=[DataRequired(), Length(max=50)])
    newPassword = PasswordField("New password", validators=[DataRequired(), Length(max=50)])
    confirmNewPassword = PasswordField("Confirm new password", validators=[DataRequired(), Length(max=50), EqualTo("newPassword", "Passwords must match.")])
    submit = SubmitField("Update password")

class RecoverAccountForm(FlaskForm):
    email = EmailField("Email Address", validators=[DataRequired()])
    submit = SubmitField("Send recovery code")

class RecoverResetPasswordForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    newPassword = PasswordField("New password", validators=[DataRequired(), Length(max=50)])
    confirmNewPassword = PasswordField("Confirm new password", validators=[DataRequired(), Length(max=50), EqualTo("newPassword", "Passwords must match.")])
    submit = SubmitField("Reset password")
