from flask import Flask
from configuration import db, SECRET_KEY
# blueprint imports
from routes.root import rootBp
"""app = Flask(__name__)
app.register_blueprint(rootBp)"""

# instantiates the flask app, registers the required blueprints
def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cs139.db"
    app.register_blueprint(rootBp)
    with app.app_context():
        db.init_app(app)

    return app



### SERVER CODE (python, flask, jinja, flask-sqlalchemy, etc.)
#route to the index

