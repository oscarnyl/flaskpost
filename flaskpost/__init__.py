""" __init__.py: Sets up Flaskpost and imports all additional pieces """
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "You should change this before using flaskpost."
#TODO: Find better home for database file?
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/flaskpost.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
from flaskpost.model import Metadata
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

import flaskpost.api
import flaskpost.paths
