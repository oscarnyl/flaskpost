#!/usr/bin/python

import sqlite3
from flask import Flask
app = Flask(__name__)

conn = sqlite3.connect("posts.db")

@app.route("/")
def blog():
    result = []
    cursor = conn.cursor()
    cursor.execute("SELECT post FROM blogposts")
    for (post,) in cursor.fetchall():
        result.append(post + "<br>\n")

    return "".join(result)

if __name__ == "__main__":
    app.run()
