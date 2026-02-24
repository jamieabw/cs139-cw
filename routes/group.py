from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug import security
from configuration import db
from models import Groups, GroupMembers, Bills, Debtors, Payments
from forms import CreateBillForm

groupBp = Blueprint("group", __name__, url_prefix="/group")


"""
checks if a group exists, if it doesn't then returns a 404, else it checks if the user belongs to the group
and if they do, allows them to view the group page, allows dynamic group page loading through one html template
"""
@groupBp.route("/<int:id>", methods=["GET", "POST"])
@login_required
def groupPage(id: int):
    form = CreateBillForm()
    group = Groups.query.get_or_404(id)
    if form.validate_on_submit():
        amount = form.amount.data
        desc = form.description.data
        try:
            """NOTE:
            THIS IS TEMPORARY PLACEHOLDER!!!!
            """
            newBill = Bills(current_user.id, id, desc, amount)
            db.session.add(newBill)
            numMembers = len(GroupMembers.query.filter_by(groupId=id).all())
            for userMember in GroupMembers.query.filter_by(groupId=id):
                userId = userMember.userId
                db.session.add(Debtors(newBill.id, userId, 100 / numMembers, amount / numMembers))
            db.session.commit()
            print("success")
        except Exception as e:
             print(e)
             db.session.rollback()
    for groupMember in GroupMembers.query.filter_by(groupId=id):
            if groupMember.userId == current_user.id:
                return render_template("groupPage.html", group=group, form=form, bills=Bills.query.filter_by(groupId=id).all())
    return redirect(url_for("root.joinGroup"))


@groupBp.route("/<int:groupId>/bill/<int:billId>", methods=["GET", "POST"])
@login_required
def groupBillPage(groupId: int, billId: int):
    bill = Bills.query.filter_by(id=billId).first_or_404()
    if bill.groupId != groupId:
         return "404"#redirect(url_for("root.joinGroup"))
    for groupMember in GroupMembers.query.filter_by(groupId=groupId):
            if groupMember.userId == current_user.id:
                debtors = Debtors.query.filter_by(billId=billId).all()
                payments = Payments.query.filter_by(billId = billId).all()
                return render_template("groupBill.html", bill=bill, debtors=debtors, payments=payments)
    return redirect(url_for("root.joinGroup"))

