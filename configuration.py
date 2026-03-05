from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os
db = SQLAlchemy()
loginManager = LoginManager()
SECRET_KEY = "secretkey"
mail = Mail()
sender = f"{os.getlogin()}@dcs.warwick.ac.uk"
