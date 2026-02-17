from flask import Blueprint, render_template

rootBp = Blueprint("root", __name__, url_prefix="")

@rootBp.route("/")
def root():
    return render_template("test.html")

@rootBp.route("/login")
def login():
    return render_template("login.html")