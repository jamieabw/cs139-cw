from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
rootBp = Blueprint("root", __name__, url_prefix="")

@rootBp.route("/")
@login_required
def index():
    return render_template("index.html")
