from functools import wraps

__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = 'Franklyn Tackitt'
__license__ = 'MIT/X11'
__copyright__ = '(c) 2013 by Franklyn Tackitt'
__all__ = ['Sandbox']


class Sandbox(object):

    """
    This object restricts users to a sandboxed area of the site,
    based on restrictions determined by their User object
    """
    _app = None

    def __init__(self, app=None):
        """Initializes the sandbox against the app"""
        from flask import abort
        from flask.ext.login import current_user
        self.abort = abort
        self.current_user = current_user
        if app is not None:
            self.init_app(app)

    def __call__(self, filter, result=None, *args, **kwargs):
        """A decorator for a single route, to restrict to a filter"""
        def decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                if not self.current_user.is_authenticated() \
                        or not filter(self.current_user):
                    return result or self.abort(403)
                return fn(*args, **kwargs)
            return wrapper
        return decorator

    def setup_app(self, app=None):
        """deprecated setup_app"""
        import warnings
        warnings.warn('Warning setup_app is deprecated. Please use init_app')
        self.init_app(app)

    def init_app(self, app=None):
        """Init the sandbox against the app"""
        app.sandbox = self
        self._app = app

    def register_blueprint(self, blueprint, filter=None, result=None,
                           *args, **kwargs):
        """Registers a blueprint to the app, with a specified filter.
        If result is given, returns that, otherwise, 403"""
        if filter:
            @blueprint.before_request
            def before_blueprint():
                if not self.current_user.is_authenticated() \
                        or not filter(self.current_user):
                    return result or self.abort(403)
        self._app.register_blueprint(blueprint, *args, **kwargs)
