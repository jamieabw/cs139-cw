from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug import security
from configuration import db
from models import Groups, GroupMembers
rootBp = Blueprint("root", __name__, url_prefix="")

@rootBp.route("/")
@login_required
def index():
    usersGroups = []
    for group in GroupMembers.query.filter_by(userId=current_user.id):
        print(Groups.query.filter_by(id=group.id).first().name) # temp
        usersGroups.append(Groups.query.filter_by(id=group.id).first())
    return render_template("index.html", groups=usersGroups)

# these two group creation and join routes are temporary, they will be replaced with a pop up form.
@rootBp.route("/createGroup", methods=["GET", "POST"])
@login_required
def createGroup():
    if request.method == "GET":
        return render_template("createGroupTemp.html")
    else:
        try:
            groupName = request.form["groupName"]
            groupPassword = security.generate_password_hash(request.form["groupPassword"])
            db.session.add(Groups(groupName, groupPassword))

            db.session.add(GroupMembers(current_user.id, Groups.query.filter_by(name=groupName).first().id))
            db.session.commit()
            print("group added!")
            return redirect(url_for(".index"))
        except Exception:
            db.session.rollback()
            return render_template("createGroupTemp.html")


@rootBp.route("/joinGroup")
@login_required
def joinGroup():
    return render_template("joinGroupTemp.html")