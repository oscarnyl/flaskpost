#!/usr/bin/python

import sqlite3
import datetime
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

conn = sqlite3.connect("posts.db")

""" Inserts a post into the database, then redirects to the blog front page. """
@app.route("/api/post", methods=["POST"])
def api_post():
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
    result = []
    cursor = conn.cursor()
    cursor.execute("SELECT title, post, date FROM blogposts")
    for (title, post, date,) in cursor.fetchall():
        result.append((title, post, date))

    return render_template("index.html", content=result)

""" Serves a page where blog posts can be inserted into the database. """
@app.route("/post")
def blog_post():
    return render_template("post.html")

if __name__ == "__main__":
    app.run()
