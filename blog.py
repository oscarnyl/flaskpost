#!/usr/bin/python

import sqlite3
from flask import Flask, render_template
app = Flask(__name__)

conn = sqlite3.connect("posts.db")

@app.route("/")
def blog():
    result = []
    cursor = conn.cursor()
    cursor.execute("SELECT title, post, date FROM blogposts")
    for (title, post, date,) in cursor.fetchall():
        result.append((title, post, date))

    return render_template("index.html", content=result)

if __name__ == "__main__":
    app.run()
