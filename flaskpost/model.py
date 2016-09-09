""" model.py - contains all ORM representations used """
import datetime
from flaskpost import db
from flask_login import UserMixin
from passlib.hash import sha256_crypt

""" ORM Representation of a Blogpost.  """
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    post = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)

    def __init__(self, title, post):
        self.title = title
        self.post = post
        self.date = datetime.datetime.now()

""" ORM Representation of a Metadata Key-Value pair. """
class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Text, nullable=False)
    value = db.Column(db.Text, nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value

""" ORM Representation of a User, with a UserMixin to allow compatibility with
    Flask-Login. """
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, username, password, active=True):
        self.username = username
        # Passwords get stored as salted hashes.
        self.password = sha256_crypt.encrypt(password)
