from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug import security
from configuration import db, loginManager
from models import Users, Debtors
from forms import RegisterForm, LoginForm

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

@accountBp.route("/debts")
@login_required
def debts():
    return render_template("debts.html", debts=Debtors.query.filter_by(userId=current_user.id).all())


@accountBp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))