from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug import security
from configuration import db, loginManager
from models import Users

accountBp = Blueprint("account", __name__, url_prefix="/account")

@loginManager.user_loader
def loadUser(userId):
    return db.session.get(Users, int(userId))

@accountBp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST": # if the form has been submitted, get the values and store them in the db
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password = security.generate_password_hash(password)
        try:
            db.session.add(Users(username, email, password))
            db.session.commit()
            userFound = Users.query.filter_by(username=request.form["username"]).first()
            login_user(loadUser(userFound.id))
        except Exception:
            db.session.rollback()
            # flash a message here when you figure that out, for now just redirect back to register
            return redirect(url_for(".register"))
        return redirect(url_for("root.index"))
    

@accountBp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user:
            redirect(url_for("root.index"))
        return render_template("login.html")
    elif request.method == "POST":
        userFound = Users.query.filter_by(username=request.form["username"]).first()
        if userFound and security.check_password_hash(userFound.password, request.form["password"]):
             # user details match the db's
            login_user(loadUser(userFound.id))
            return redirect(url_for("root.index"))
        else:
            # flash an incorrect details message
            return render_template("login.html")


@accountBp.route("/manage")
@login_required
def manage():
    return render_template("manageAccount.html")


@accountBp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".register"))