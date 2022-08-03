"""
This module is an example of
how to use the Flask-Sustainable package.

It is a simple Flask application that uses the Flask-Sustainable package.
"""

import flask

from flask_sustainable import Sustainable
from flask_sustainable.indicator import PerfCPU, PerfRAM, PerfTime


def create_app() -> flask.Flask:
    """Create and configure an instance of the Flask application.

    This is a simple Flask application that uses the Flask-Sustainable package.

    :return: Flask application instance
    """
    app = flask.Flask(__name__)
    sustainable = Sustainable(app)
    sustainable.add_indicator(PerfTime())
    sustainable.add_indicator(PerfCPU())
    sustainable.add_indicator(PerfRAM())

    @app.route("/")
    def _():
        return "Hello, World!"

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
