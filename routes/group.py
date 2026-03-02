from flask import Blueprint, render_template, redirect, url_for, request, jsonify, abort
from flask_login import login_required, current_user
from werkzeug import security
from configuration import db
from models import Groups, GroupMembers, Bills, Debtors, Payments, Users
from forms import CreateBillForm

groupBp = Blueprint("group", __name__, url_prefix="/group")


def setMemberProportionFields(groupId: int, form: object):
    form.proportions.entries = []
    for groupMember in GroupMembers.query.filter_by(groupId=groupId):
        entry = {}
        entry["memberId"] = groupMember.userId
        entry["memberName"] = Users.query.filter_by(id=groupMember.userId).first().username
        form.proportions.append_entry(entry)
        


"""
Checks if the user is in the group or if the user is the admin, returns true if that is the case
"""
def checkIfUserInGroup(groupId: int):
    for groupMember in GroupMembers.query.filter_by(groupId=groupId):
            if groupMember.userId == current_user.id or current_user.username == "admin":
                return True
    return False

"""
Creates a dictionary which stores billId : whether all debtors have paid,
passed into the html to determine whether the bill is current or previous
"""
def createSettledBillsMap(groupId: int):
    bills = Bills.query.filter_by(groupId=groupId).all()
    settledBillMap = {}
    for bill in bills:
        debts = Debtors.query.filter_by(billId=bill.id).all()
        if all(debt.status == "paid" for debt in debts):
             settledBillMap[bill.id] = True
        else:
             settledBillMap[bill.id] = False
    return settledBillMap


@groupBp.route("/<int:id>/delete")
@login_required
def deleteBill(id: int):
    # need to drop the bill, drop all payments
    billToDelete = Bills.query.filter_by(id=id).first()
    groupId = billToDelete.groupId
    if not checkIfUserInGroup(groupId):
        redirect(url_for("group.joinGroup"))
    try:
        for payment in Payments.query.filter_by(billId=billToDelete.id).all():
            db.session.delete(payment)
        for debtor in Debtors.query.filter_by(billId=billToDelete.id):
            db.session.delete(debtor)
        db.session.delete(billToDelete)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return redirect(url_for(".groupPage", id=groupId))


"""
checks if a group exists, if it doesn't then returns a 404, else it checks if the user belongs to the group
and if they do, allows them to view the group page, allows dynamic group page loading through one html template
"""
@groupBp.route("/<int:id>", methods=["GET", "POST"])
@login_required
def groupPage(id: int):
    form = CreateBillForm()
    group = Groups.query.get_or_404(id)
    settledBillsMap = createSettledBillsMap(id)
    if request.method == "GET":
        setMemberProportionFields(id, form)
    if form.validate_on_submit():
        total = float(form.total.data)
        desc = form.description.data
        proportions = {}
        """
        {% for proportion in form.proportions %}
                                <div>
                                    <span>{{proportion.memberName.data}}</span>
                                    <span class="percent" data-for="{{proportion.proportion.id}}"></span>%
                                    {{proportion.memberId()}}
                                    {{proportion.memberName()}}
                                    <div>{{proportion.proportion(oninput="update(this)")}}</div>
                                </div>
        """
        for proportion in form.proportions:
            proportions[int(proportion.memberId.data)] = int(proportion.proportion.data)

        try:
            print("TEST 2")
            newBill = Bills(current_user.id, id, desc, total)
            db.session.add(newBill)
            for userMember in GroupMembers.query.filter_by(groupId=id):
                userId = userMember.userId
                db.session.add(Debtors(newBill.id, userId, proportions[userId], total * (proportions[userId] / 100)))
            db.session.commit()
            print("it worked allegedly")
        except Exception as e:
             print(e)
             print("WRONG WO+")
             db.session.rollback()
        return redirect(url_for(".groupPage", id=id))
    if checkIfUserInGroup(id) is True:
        return render_template("groupPage.html", group=group, form=form, bills=Bills.query.filter_by(groupId=id).all(), settledBillMap=settledBillsMap)
    return redirect(url_for("root.joinGroup"))


@groupBp.route("/<int:groupId>/bill/<int:billId>", methods=["GET", "POST"])
@login_required
def groupBillPage(groupId: int, billId: int):
    bill = Bills.query.filter_by(id=billId).first_or_404()
    if bill.groupId != groupId:
        abort(404)
    if checkIfUserInGroup(groupId) is not True:
        return redirect(url_for("root.joinGroup"))
    form = CreateBillForm(obj=bill)
    if request.method == "GET":
        setMemberProportionFields(groupId, form)
    debtors = Debtors.query.filter_by(billId=billId).all()
    payments = Payments.query.filter_by(billId = billId).all()
    form.submit.label.text = "Save bill" #just so i can reuse the same form
    return render_template("groupBill.html", bill=bill, payments=payments, debtors=debtors, form=form)


"""
AJAX implementation for editing the bill, should probably figure out how to close the form afterwards
"""
@groupBp.route("/edit/<billId>", methods=["POST"])
def editBill(billId: int, form):
    # need the action to point here.
    data = request.get_json()
    #billId = data["billId"]
    description = data["description"]
    total = float(data["total"])
    billToEdit = Bills.query.filter_by(id=billId).first_or_404()
    print(data, billId, description, total)
    for groupMember in GroupMembers.query.filter_by(groupId=billToEdit.groupId).all():
        if Debtors.query.filter_by(userId=groupMember.userId).first() is None: # checks whether any new members have been added
            db.session.add(Debtors(billToEdit.id, groupMember.userId, 0, 0))
    numMembers = len(GroupMembers.query.filter_by(groupId=billToEdit.groupId).all())
    proportions = {}
    for proportion in form.proportions:
            proportions[int(proportion.memberId.data)] = int(proportion.proportion.data)
            print(proportions)
    try:
        billToEdit.description = description
        billToEdit.total = total
        for payment in Payments.query.filter_by(billId=billId).all():
            db.session.delete(payment)
        for debtor in Debtors.query.filter_by(billId=billId).all():
            debtor.status = "unpaid"
            debtor.proportion = 100 / numMembers # can change this eventually when proportional
            debtor.owed = total / numMembers
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return jsonify({"ok": True, "billId": billId})

"""
NOTE: apparently something like this will fix my worries, just need to pass the form instead of the json.

@groupBp.route("/edit/<int:billId>", methods=["POST"])
@login_required
def editBill(billId: int):
    form = CreateBillForm()  # binds from request.form automatically

    if not form.validate_on_submit():
        return jsonify({"ok": False, "errors": form.errors}), 400

    proportions = {}
    for p in form.proportions:
        proportions[int(p.memberId.data)] = float(p.proportion.data)

    # now use proportions dict in your Debtors update
    ...
    return jsonify({"ok": True, "billId": billId})

"""


"""
AJAX backend for updating the debtors within the bill page after editing the bill
"""
@groupBp.route("/bill/<int:billId>/debtorsData")
def debtorsData(billId: int):
    print("hello world")
    debtors = Debtors.query.filter_by(billId=billId).all()
    data = [{"username": d.user.username,"proportion": float(d.proportion), "owed": float(d.owed)} for d in debtors]
    print(data)
    return jsonify({"debtors": data}) # sp this can be passed back into the HTML to update the grid


"""
first AJAX implementation, checks the action data of the button clicked and updates DB accordingly
"""
@groupBp.route("/payment/action", methods=["POST"])
@login_required
def resolveAction():
    data = request.get_json()
    paymentId = data["paymentId"]
    action = data["action"]
    payment = Payments.query.filter_by(id=paymentId).first()
    debt = Debtors.query.filter_by(billId=payment.billId, userId=payment.payerId).first()
    if action == "ack": # acknowledgin the payment
        print(payment.payerId, "ack")
        try:
            payment.status = "acknowledged"
            debt.status = "paid"
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()         
    elif action == "rej":
        print(payment.payerId, "rej")
        try:
            payment.status = "rejected"
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        ...
    return jsonify({"ok": True})

