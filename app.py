from flask import Flask, render_template
from routes.root import rootBp

app = Flask(__name__)
app.register_blueprint(rootBp)




### SERVER CODE (python, flask, jinja, flask-sqlalchemy, etc.)
#route to the index


"""@app.route('/')
def index():
    with open('README.md') as readme:
      with open('requirements.txt') as req:
        return render_template('index.html', README=readme.read(), requirements=req.read())"""
