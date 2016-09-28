#!/usr/bin/python
""" run.py: Starts a Flaskpost session. """

from flaskpost import app
from flaskpost.additional import ConfigSingleton

if __name__ == "__main__":
    config = ConfigSingleton()
    app.run()
