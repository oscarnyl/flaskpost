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

""" Singleton to load and contain the configuration of the blog. """
class ConfigSingleton:
    class __ConfigSingleton:
        needs_setup = None
        title = None
        def __init__(self, title=None, needs_setup=None):
            if title == None and needs_setup == None:
                self.needs_setup =\
                (Metadata.query.filter_by(key="setup_reverse_canary").first() ==\
                None)
                if not self.needs_setup:
                    self.title =\
                    Metadata.query.filter_by(key="blog_title").first().value
            else:
                self.title = title
                self.needs_setup = needs_setup

    instance = None
    def __init__(self):
        if not ConfigSingleton.instance:
            ConfigSingleton.instance = ConfigSingleton.__ConfigSingleton()

    # Pass all attribute access to the inner class.
    def __getattr__(self, name):
        return getattr(self.instance, name)

    def update(self, title, needs_setup):
        ConfigSingleton.instance = ConfigSingleton.__ConfigSingleton(title, needs_setup)

import flaskpost.api
import flaskpost.paths
