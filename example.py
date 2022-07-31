"""
This module is an example of
how to use the Flask-Sustainable package.

It is a simple Flask application that uses the Flask-Sustainable package.
"""

import flask

from flask_sustainable import Sustainable


def create_app() -> flask.Flask:
    """Create and configure an instance of the Flask application.

    This is a simple Flask application that uses the Flask-Sustainable package.

    :return: Flask application instance
    """
    app = flask.Flask(__name__)
    Sustainable(app)

    @app.route("/")
    def _():
        return "Hello, World!"

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
