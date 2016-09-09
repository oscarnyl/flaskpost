""" paths.py: Contains all browseable paths. """
from flask import render_template, redirect
from flask_login import login_required

from flaskpost import app, ConfigSingleton
from flaskpost.decorators import ssl_required
from flaskpost.model import Blogpost

config = ConfigSingleton()

""" Serves a page where users can log in. """
@app.route("/login")
@ssl_required
def login():
    if config.needs_setup:
        return redirect("/setup")
    return render_template("login.html", blog_title=config.title)

""" Serves the setup page. This page will in turn call "/api/setup". """
@app.route("/setup")
@ssl_required
def setup():
    return render_template("setup.html", blog_title="Setup")

""" Gets 10 blog-posts from database, then serves them in a page. """
@app.route("/")
def blog_main():
    if config.needs_setup:
        return redirect("/setup")
    result = []
    for post in Blogpost.query.limit(10):
        result.append((post.id, post.title, post.post, post.date))

    return render_template("index.html", content=result,
            blog_title=config.title)

""" Serves a page where blog posts can be inserted into the database. """
@app.route("/post")
@login_required
def blog_post():
    if config.needs_setup:
        return redirect("/setup")
    return render_template("post.html", blog_title=config.title)
