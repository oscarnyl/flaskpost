""" decorators.py: contains all additional decorators """
from functools import wraps
from flask import current_app, redirect, request

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
