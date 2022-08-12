# coding: utf-8

"""This module represents examples of score implementation.

For more information about what a score, see :class:`BaseScore` class.
"""

import logging

import flask

from flask_sustainable.base import BaseScore


class PerfScoreCO2(BaseScore):
    """Score that measure the CO2 emissions of the request.

    When the request is done, the response will contain a header named "Perf-Score-1"
    with an equivalent of CO2 emissions of the request in kilograms.

    The CO2 emissions are the emissions of the process
    that is different from the execution time.

    Example ::

        from flask_sustainable import Sustainable
        from flask_sustainable.score import PerfScoreCO2

        app = flask.Flask(__name__)
        sustainable = Sustainable(app)
        sustainable.add_score(PerfScoreCO2())
    """

    name = "Perf-Score-1"

    def after_request(self, response: flask.Response) -> flask.Response:
        try:
            final_emissions = flask.g.tracker.final_emissions
            if final_emissions:
                response.headers.update({self.name: f"{final_emissions:.16f}"})
        except AttributeError:
            logging.warning("No tracker found in flask.g")
        return response
