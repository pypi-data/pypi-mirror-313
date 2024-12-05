"""
    Gunicorn Server Wrapper.

    This class extends MLServerInterface and provides a wrapper for starting a Gunicorn server using the BaseApplication class.
    It allows easy integration of Gunicorn with a Flask application.

    Methods:
        - __init__: Initialize the GunicornServer instance.
        - start: Start the Gunicorn server.
        - stop: Stop the Gunicorn server (Not implemented).
        - reload: Reload the Gunicorn server.
        - load: Load the Flask application.
"""

import gunicorn.app.base
from .ml_server_interface import MLServerInterface

class GunicornServer(MLServerInterface):

    def __init__(self, app, options=None):
        """
        Initialize the GunicornServer instance.

        Parameters:
            - app: The Flask application instance.
            - options (dict): Optional Gunicorn configuration options.
        """
        self.gunicorn_app = GunicornBaseApplication(app, options)

    def start(self):
        """Start the Gunicorn server."""
        self.gunicorn_app.run()

    def stop(self):
        """Stop the Gunicorn server."""
        pass

    def reload(self):
        """Reload the Gunicorn server."""
        self.gunicorn_app.reload()

    def load(self):
        """Load the Flask application."""
        pass

class GunicornBaseApplication(gunicorn.app.base.BaseApplication):
    """
    Gunicorn Base Application Wrapper. see https://github.com/benoitc/gunicorn/blob/master/gunicorn/app/base.py

    This class provides a wrapper for starting a Gunicorn server using the BaseApplication class.
    It allows easy integration of Gunicorn with a Flask application.

    Methods:
        - __init__: Initialize the GunicornServer instance.
        - load_config: Load Gunicorn configuration from options.
        - load: Load the Flask application (required by the BaseApplication class).
    """

    def __init__(self, app, options=None):
        """
        Initialize the GunicornServer instance.

        Parameters:
            - app: The Flask application instance.
            - options (dict): Optional Gunicorn configuration options.
        """
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        """Load Gunicorn configuration from options."""
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        """Load the Flask application (required by the BaseApplication class)."""
        return self.application
