from flask import Flask, render_template
from configuration import db, SECRET_KEY, loginManager, mail
from routes.root import rootBp
from routes.account import accountBp
from routes.group import groupBp
from models import Notifications
from flask_login import current_user
from flask_mail import Mail
from forms import JoinGroupForm, CreateGroupForm

"""app = Flask(__name__)
app.register_blueprint(rootBp)"""

"""instantiates the flask app, registers the required blueprints, registers configurations.
"""
def create_app():
    app = Flask(__name__)
    app.config['MAIL_SUPPRESS_SEND'] = False
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cs139db.sqlite3"
    db.init_app(app)
    mail.init_app(app)
    loginManager.init_app(app)
    loginManager.login_view = "account.login"
    app.register_blueprint(rootBp)
    app.register_blueprint(accountBp)
    app.register_blueprint(groupBp)
    with app.app_context():
        db.create_all()

    @app.context_processor
    def injectGlobals():
        if not current_user.is_authenticated:
            return {"notifications": [],
                    "createGroupForm" : CreateGroupForm(),
                    "joinGroupForm" : JoinGroupForm()}
        return {
            "notifications": Notifications.query.filter_by(userId=current_user.id).all(),
            "createGroupForm" : CreateGroupForm(),
            "joinGroupForm" : JoinGroupForm()
                }
    
    @app.errorhandler(404)
    def error404(error):
        return render_template("404.html"), 404
    
    @app.errorhandler(403)
    def error403(error):
        return render_template("403.html"), 403

    return app




