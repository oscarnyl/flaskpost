#!/usr/bin/python
""" run.py: Starts a Flaskpost session. """

from flaskpost import app, ConfigSingleton

if __name__ == "__main__":
    config = ConfigSingleton()
    app.run()
