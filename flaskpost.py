#!/usr/bin/python

import sqlite3
import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, redirect, abort
from flask_login import (LoginManager, UserMixin, login_required, login_user,
        logout_user)

app = Flask(__name__)
app.secret_key = "You should change this before using flaskpost."
#TODO: Find better home for database file?
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/flaskpost.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)

""" Flask-Login needs this to load users properly. """
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

""" Checks credentials, then logs in user if correct. """
@app.route("/api/login", methods=["POST"])
def api_login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()
    if sha256_crypt.verify(password, user.password):
        login_user(user)
        return redirect("/")
    else:
        return abort(401)

""" Logs out the currently logged in user. """
@app.route("/api/logout")
@login_required
def api_logout():
    logout_user()
    return redirect("/")

""" Saves settings to database metadata table, then redirects to main. """
@app.route("/api/setup", methods=["POST"])
def api_setup():
    global blog_title_global
    global needs_setup

    blog_title = request.form["blog_title"]
    admin_username = request.form["admin_username"]
    admin_password = request.form["admin_password"]

    db.session.add(Metadata("blog_title", blog_title))
    db.session.add(Metadata("setup_reverse_canary", "present"))
    db.session.add(User(admin_username, admin_password))
    db.session.commit()

    blog_title_global = blog_title
    needs_setup = False

    return redirect("/")

""" Inserts a post into the database, then redirects to the blog front page.
    Blogpost data is retrieved through a web form (served at /post), with a
    timestamp generated inside the function. """
@app.route("/api/post", methods=["POST"])
@login_required
def api_post():
    title = request.form["title"]
    postbody = request.form["postbody"]

    db.session.add(Blogpost(title, postbody))
    db.session.commit()

    return redirect("/")

""" Serves a page where users can log in. """
@app.route("/login")
def login():
    return render_template("login.html", blog_title=blog_title_global)

""" Serves the setup page. This page will in turn call "/api/setup". """
@app.route("/setup")
def setup():
    return render_template("setup.html", blog_title="Setup")

""" Gets all blog-posts from database, then serves them in a page. """
@app.route("/")
def blog_main():
    if needs_setup:
        return redirect("/setup")
    result = []
    for post in Blogpost.query.all():
        result.append((post.title, post.post, post.date))

    return render_template("index.html", content=result,
            blog_title=blog_title_global)

""" Serves a page where blog posts can be inserted into the database. """
@app.route("/post")
@login_required
def blog_post():
    if needs_setup:
        return redirect("/setup")
    return render_template("post.html", blog_title=blog_title_global)

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

    def __init__(self, username, password, active):
        self.username = username
        # Passwords get stored as salted hashes.
        self.password = sha256_crypt.encrypt(password)

if __name__ == "__main__":
    # If setup_reverse_canary is not present, this evaluates to true.
    needs_setup = (Metadata.query.filter_by(key="setup_reverse_canary").first() == None)
    if not needs_setup:
        blog_title_global =\
        Metadata.query.filter_by(key="blog_title").first().value
    app.run()
