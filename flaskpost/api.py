""" api.py: Contains all API-paths. """
#TODO: Make API client-agnostic
from flaskpost import app, login_manager, db
from flaskpost.model import Blogpost, Metadata, User
from flaskpost.additional import ssl_required, ConfigSingleton

from flask import request, redirect
from flask_login import login_required, login_user, logout_user
from passlib.hash import sha256_crypt
import json

""" Flask-Login needs this to load users properly. """
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/api/more_posts", methods=["POST"])
def api_more_posts():
    current_limit = request.get_json()["current_limit"] + 1
    result = []
    posts = Blogpost.query.all()
    filtered_posts = [post for post in posts if post.id >= current_limit and post.id <= current_limit + 10]
    for post in filtered_posts:
        result.append((post.id, post.title, post.post, post.date))
    return json.JSONEncoder().encode(result)

""" Checks credentials, then logs in user if correct. """
@app.route("/api/login", methods=["POST"])
@ssl_required
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
@ssl_required
def api_setup():
    blog_title = request.form["blog_title"]
    admin_username = request.form["admin_username"]
    admin_password = request.form["admin_password"]

    db.session.add(Metadata("blog_title", blog_title))
    db.session.add(Metadata("needs_setup", False))
    db.session.add(User(admin_username, admin_password))
    db.session.commit()

    config = ConfigSingleton()
    config.update(blog_title, False)

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

@app.route("/api/admin", methods=["POST"])
@login_required
def api_admin():
    title = request.form["blog_title"]

    config = ConfigSingleton()
    config.update(title, False)

    return redirect("/")
