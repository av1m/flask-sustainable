"""Class test for score.py module."""

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest

from flask import Flask

from flask_sustainable import Sustainable
from flask_sustainable.indicator import PerfEnergy
from flask_sustainable.score import PerfScoreCO2


class PerfScore2TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.sustainable = Sustainable(self.app)
        self.sustainable.add_score(PerfScoreCO2())

        @self.app.route("/")
        def _():
            return "Welcome!"

    def test_nothing(self):
        with self.app.test_client() as client:
            response = client.get("/")
            self.assertIsNone(response.headers.get(PerfScoreCO2.name))
            response = client.get("/", headers={"perf": "perf-energy,perf-score-1"})
            self.assertIsNone(response.headers.get(PerfScoreCO2.name))

    def test_something(self):
        self.sustainable.add_indicator(PerfEnergy())
        with self.app.test_client() as client:
            response = client.get("/", headers={"perf": "perf-energy,perf-score-1"})
            print(response.headers)
            self.assertIsNotNone(response.headers.get(PerfScoreCO2.name))
