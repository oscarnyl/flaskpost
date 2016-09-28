""" additional.py: contains all additional classes and functions commonly used
throughout flaskpost. """
from functools import wraps
from flask import current_app, redirect, request
from flaskpost.model import Metadata

""" Decorator to force SSL on certain requests.
    Source: http://flask.pocoo.org/snippets/93 """
def ssl_required(function):
    @wraps(function)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("SSL"):
            if request.is_secure:
                return function(*args, **kwargs)
            else:
                return redirect(request.url.replace("http://", "https://"))

        return function(*args, **kwargs)
    return decorated_view

""" Singleton to load and contain the configuration of the blog. """
class ConfigSingleton:
    class __ConfigSingleton:
        needs_setup = None
        title = None
        def __init__(self, title=None, needs_setup=None):
            if title == None and needs_setup == None:
                #TODO: This is an ugly hack. It needs to be replaced
                self.needs_setup =\
                (Metadata.query.filter_by(key="setup_reverse_canary").first() ==\
                None)
                if not self.needs_setup:
                    self.title =\
                    Metadata.query.filter_by(key="blog_title").first().value
            else:
                self.title = title
                self.needs_setup = needs_setup

    instance = None
    def __init__(self):
        if not ConfigSingleton.instance:
            ConfigSingleton.instance = ConfigSingleton.__ConfigSingleton()

    # Pass all attribute access to the inner class.
    def __getattr__(self, name):
        return getattr(self.instance, name)

    def update(self, title, needs_setup):
        ConfigSingleton.instance = ConfigSingleton.__ConfigSingleton(title, needs_setup)
