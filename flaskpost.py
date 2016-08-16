#!/usr/bin/python

import sqlite3
import datetime
import os
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, redirect, abort
app = Flask(__name__)

DATABASE_NAME = "blog.db"

needs_setup = False
conn = None
blog_title_global = None

# If the database does not exist, setup needs to be done.
if not os.path.isfile(DATABASE_NAME):
    needs_setup = True
else:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM metadata WHERE key='blog_title'")
    (blog_title_global,) = cursor.fetchone()

""" Serves the setup page. This page will in turn call "/api/setup". """
@app.route("/setup")
def setup():
    #TODO: Replace this with a login system
    if not needs_setup:
        abort(403) # No setup is actually needed. Abort mission.
    return render_template("setup.html", blog_title="Setup")

""" Saves settings into config file, then sets up database. """
@app.route("/api/setup", methods=["POST"])
def api_setup():
    global needs_setup
    global conn
    global blog_title_global

    #TODO: Replace this with a login system
    if not needs_setup:
        abort(403) # No setup is actually needed. Abort mission.

    blog_title_local = request.form["blog_title"]
    admin_username = request.form["admin_username"]
    admin_password = request.form["admin_password"]
    password_hash = sha256_crypt.encrypt(admin_password)

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE blogposts (id INT PRIMARY KEY, title
    TEXT NOT NULL, post TEXT NOT NULL, date TEXT NOT NULL);
    CREATE TABLE metadata (key TEXT NOT NULL, value TEXT NOT NULL);
    CREATE TABLE users (id INT PRIMARY KEY, username TEXT NOT NULL,
    password TEXT NOT NULL);
    """)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            (admin_username, password_hash,))
    cursor.execute("INSERT INTO metadata (key, value) VALUES (?, ?)",
    ("blog_title", blog_title_local,))
    blog_title_global = blog_title_local

    conn.commit()
    needs_setup = False
    return redirect("/")

""" Inserts a post into the database, then redirects to the blog front page.
    Blogpost data is retrieved through a web form (served at /post), with a
    timestamp generated inside the function. """
@app.route("/api/post", methods=["POST"])
def api_post():
    #TODO: Disallow access for unauthorized users
    if needs_setup:
        return redirect("/setup")

    title = request.form["title"]
    postbody = request.form["postbody"]
    timestamp = datetime.datetime.now()

    cursor = conn.cursor()
    cursor.execute("INSERT INTO blogposts (title, post, date) VALUES (?, ?, ?)",
            (title, postbody, timestamp,))
    conn.commit()

    return redirect("/")

""" Gets all blog-posts from database, then places them into a template. """
@app.route("/")
def blog_main():
    if needs_setup:
        return redirect("/setup")

    result = []
    cursor = conn.cursor()
    cursor.execute("SELECT title, post, date FROM blogposts")
    for (title, post, date,) in cursor.fetchall():
        result.append((title, post, date))

    return render_template("index.html", content=result,
            blog_title=blog_title_global)

""" Serves a page where blog posts can be inserted into the database. """
@app.route("/post")
def blog_post():
    #TODO: Disallow access for unauthorized users
    if needs_setup:
        return redirect("/setup")

    return render_template("post.html", blog_title=blog_title_global)

if __name__ == "__main__":
    app.run()
