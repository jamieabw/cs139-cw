from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug import security
from configuration import db, loginManager, mail, sender
from models import Users, Debtors, Payments, Notifications, LoginAttemptLogs, BillLog
from forms import RegisterForm, LoginForm, SettleDebtForm, RecoverAccountForm, RecoverResetPasswordForm, updateAccountDetailsForm, updatePasswordForm
import random

accountBp = Blueprint("account", __name__, url_prefix="/account")

@loginManager.user_loader
def loadUser(userId):
    return db.session.get(Users, int(userId))


"""
page for registering a new user
"""
@accountBp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = security.generate_password_hash(form.password.data)
        user = Users(username, email, password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        log = LoginAttemptLogs(user.id, "Created an account.", True)
        db.session.add(log)
        db.session.commit()
        return redirect(url_for("root.index"))
    return render_template("register.html", form=form)

    
"""
page for logging into an existing user's account
"""
@accountBp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        userFound = Users.query.filter_by(username=form.username.data).first()
        if userFound:
            if security.check_password_hash(userFound.password, form.password.data):
                login_user(loadUser(userFound.id))
                db.session.add(LoginAttemptLogs(userFound.id, "Attempted Log in.", True))
                db.session.commit()
                return redirect(url_for("root.index"))
            else:
                db.session.add(LoginAttemptLogs(userFound.id, "Attempted Log in.", False))
                db.session.commit()
    return render_template("login.html", form=form)

"""
page for managing account such as changing details, logging out, changing password
"""
@accountBp.route("/manage", methods=["GET", "POST"])
@login_required
def manage():
    accountForm = updateAccountDetailsForm()
    passwordForm = updatePasswordForm()
    if accountForm.validate_on_submit() and accountForm.submit.data:
        try:
            user = Users.query.filter_by(id=current_user.id).first()
            user.username = accountForm.username.data
            user.email = accountForm.email.data
            db.session.commit()
            return redirect(url_for(".manage"))
        except Exception as e:
            print("ERROR: ", e)
            db.session.rollback()

    if passwordForm.validate_on_submit() and passwordForm.submit.data:
        if security.check_password_hash(current_user.password, passwordForm.currentPassword.data):
            try:
                user = Users.query.filter_by(id=current_user.id).first()
                user.password = security.generate_password_hash(passwordForm.newPassword.data)
                db.session.commit()
            except Exception as e:
                print("ERROR", e)
                db.session.rollback()
        return redirect(url_for(".manage"))
    accountForm.email.data = current_user.email
    accountForm.username.data = current_user.username
    return render_template("manageAccount.html", accountForm=accountForm, passwordForm=passwordForm)

"""
a page to display the current debts the user owes
"""
@accountBp.route("/debts", methods=["GET", "POST"])
@login_required
def debts():
    form = SettleDebtForm()
    debtStatuses = {}
    for payment in Payments.query.filter_by(payerId=current_user.id).all():
        debtStatuses[payment.billId] = payment.status
    if form.validate_on_submit():
        debt = db.session.get(Debtors, (int(form.billId.data), current_user.id))
        evidence = form.evidence.data.read()
        evidenceMIME = form.evidence.data.mimetype
        payerId = current_user.id 
        payeeId = debt.bill.creator.id
        amount = debt.owed
        billId = debt.bill.id
        db.session.add(Payments(billId, payerId, payeeId, amount, evidence, evidenceMIME))
        db.session.add(BillLog(current_user.id, billId,f"Paid £{amount}"))
        if payeeId != current_user.id:
            db.session.add(Notifications(debt.bill.groupId, payeeId, current_user.id, "bill payment"))
        db.session.commit()
        return redirect(url_for(".debts"))

    
    return render_template("debts.html", debts=Debtors.query.filter_by(userId=current_user.id).all(), form=form, 
                           debtStatuses=debtStatuses)

"""
the page which contains the form for the user to put the email of the account they want to recover
"""
@accountBp.route("/recover", methods=["POST", "GET"])
def recover():
    form = RecoverAccountForm()
    if form.validate_on_submit():
 # this needs to send the code to the email, pass it into something that can store it etc
        session["email"] = form.email.data
        session["attempts"] = 0
        return redirect(url_for("account.reset"))
    return render_template("recover.html", form=form)


"""
page which contains the form for the code, and changing their password
"""
@accountBp.route("/reset", methods=["POST", "GET"])
def reset():
    session["attempts"] += 1
    if not "email" in session:
        return redirect(url_for(".recover"))
    if session["attempts"] > 3:
        session.pop("attempts", None)
        return redirect(url_for(".login"))
    email = session["email"]
    form = RecoverResetPasswordForm()
    if form.validate_on_submit():
        if form.code.data == session["code"]:
            try:
                password = security.generate_password_hash(form.newPassword.data)
                user = Users.query.filter_by(email=email).first()
                user.password = password
                db.session.commit()
                session.pop("code", None)
                session.pop("email", None)
                session.pop("attempts", None)
                return redirect(url_for("account.login"))
            except Exception as e:
                print("ERROR:", e)
                db.session.rollback()
    if Users.query.filter_by(email=email).first():
        sendRecoveryCode(email)
    return render_template("reset.html", form=form)


"""
generates 6 random digits and concatenates them together, sends them in a n email to the user to recover their account
"""
def sendRecoveryCode(email):
    code = ""
    for i in range(6):
        code += str(random.randint(0,9))
    # NOTE: SEND EMAIL HERE THE LOGIC WORKS
    subject="RECOVERY CODE"
    senders=("NOREPLY", sender)
    recipients=[email]
    body=f"Hi, here is your recovery code: {code}"
    try:
        mail.send_message(subject=subject, sender=senders, recipients=recipients,
                        body=body)
    except Exception as e:
        print("ERROR: ", e)
    #print(code)
    #print(subject, senders, recipients, body)
    session["code"] = code


"""
Logs the user out, self explanatory
"""
@accountBp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))