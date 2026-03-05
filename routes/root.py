from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from werkzeug import security
from configuration import db
from models import Groups, GroupMembers, Notifications, LoginAttemptLogs
rootBp = Blueprint("root", __name__, url_prefix="")

"""
either shows the users what groups theyre apart of, or redirects them to the login page
"""
@rootBp.route("/", methods=["GET", "POST"])
@login_required
def index():
    usersGroups = []
    for group in GroupMembers.query.filter_by(userId=current_user.id):
        #print(Groups.query.filter_by(id=group.groupId).first().name) # temp
        usersGroups.append(Groups.query.filter_by(id=group.groupId).first())
    if current_user.username == "admin":
        for group in Groups.query.all():
            if group not in usersGroups:
                usersGroups.append(group)
    return render_template("index.html", groups=usersGroups)
        
@rootBp.route("/notification/dismiss", methods=["POST"])
def dismissNoti():
    #print("I\nAM\nGETTING\n\n\n\n\nHERE")
    data = request.get_json()
    notificationId = data["notificationId"]
    userId = Notifications.query.filter_by(id=notificationId).first_or_404().userId
    try:
        db.session.delete(Notifications.query.filter_by(id=notificationId).first())
        db.session.commit()
    except Exception as e:
        print("ERROR: ", e)
        db.session.rollback()
        return jsonify({"ok" : False})
    numOfNotis = len(Notifications.query.filter_by(userId=userId).all())
    print(numOfNotis)
    return jsonify({"ok": True, "numOfNotis": numOfNotis})

@rootBp.route("/logs")
@login_required
def logs():
    if current_user.username != "admin":
        return redirect(url_for(".index"))
    return render_template("loginLogs.html", logs=LoginAttemptLogs.query.all())

@rootBp.route("/credits")
def credits():
    return render_template("credits.html")
    
        