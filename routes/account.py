from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug import security
from configuration import db, loginManager
from models import Users, Debtors, Payments, Notifications
from forms import RegisterForm, LoginForm, SettleDebtForm

accountBp = Blueprint("account", __name__, url_prefix="/account")

@loginManager.user_loader
def loadUser(userId):
    return db.session.get(Users, int(userId))

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
        return redirect(url_for("root.index"))
    return render_template("register.html", form=form)

    

@accountBp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        userFound = Users.query.filter_by(username=form.username.data).first()
        if userFound and security.check_password_hash(userFound.password, form.password.data):
            login_user(loadUser(userFound.id))
            return redirect(url_for("root.index"))
    return render_template("login.html", form=form)

@accountBp.route("/manage")
@login_required
def manage():
    return render_template("manageAccount.html")

@accountBp.route("/debts", methods=["GET", "POST"])
@login_required
def debts():
    form = SettleDebtForm()
    debtStatuses = {}
    for payment in Payments.query.filter_by(payerId=current_user.id).all():
        debtStatuses[payment.billId] = payment.status
    print(debtStatuses)
    if form.validate_on_submit(): # the issue here is figuring out which user is doing their debt, but i may be a retard and have just figured it out from typing this
        debt = db.session.get(Debtors, (int(form.billId.data), current_user.id))
        # maybe current_user can be implemented here??, no javascript is definitely needed
        evidence = form.evidence.data.read()
        payerId = current_user.id 
        payeeId = debt.bill.creator.id
        amount = debt.owed
        billId = debt.bill.id
        db.session.add(Payments(billId, payerId, payeeId, amount, evidence))
        if payeeId != current_user.id:
            db.session.add(Notifications(debt.bill.groupId, payeeId, current_user.id, "bill payment"))
        db.session.commit()
        return redirect(url_for(".debts"))

    
    return render_template("debts.html", debts=Debtors.query.filter_by(userId=current_user.id).all(), form=form, \
                           debtStatuses=debtStatuses)


@accountBp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))