"""Class test for indicator.py module."""

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest

from flask import Flask

from flask_sustainable.base import BaseHeader


class RaiseBaseTestCase(unittest.TestCase):
    class FirstBase(BaseHeader):  # pylint: disable=all
        pass

    class SecondBase(BaseHeader):
        def after_request(self, response):
            pass

    class ThirdBase(BaseHeader):
        name: str

    class FourthBase(BaseHeader):
        name: str

        def after_request(self, response):
            pass

    def test_raise(self):
        with self.assertRaises(TypeError):
            self.FirstBase()
            self.SecondBase()
            self.ThirdBase()
            self.FourthBase()


class NotRaiesBaseTestCase(unittest.TestCase):
    class FirstBase(BaseHeader):
        name: str = "Perf-Example"

        def after_request(self, response):
            pass

    def test_not_raise(self):
        self.FirstBase()


class NormalHeaderTestCase(unittest.TestCase):
    class NormalHeader(BaseHeader):
        name: str = "Perf-Example"

        def after_request(self, response):
            response.headers.update({"Perf-Example": "1.0"})
            return response

    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.NormalHeader()._init_app(self.app)

        @self.app.route("/")
        def _():
            return "Welcome!"

    def test_init_work(self):
        with self.app.test_client() as client:
            response = client.get("/")
            self.assertIn("Perf-Example", response.headers)
            self.assertEqual(response.headers["Perf-Example"], "1.0")
