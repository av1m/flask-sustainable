"""Class test for indicator.py module."""

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest

from flask import Flask

from flask_sustainable import Sustainable
from flask_sustainable.indicator import PerfCPU, PerfRAM, PerfTime


class PerfTimeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        sustainable = Sustainable(self.app)
        sustainable.add_indicator(PerfTime())

        @self.app.route("/")
        def _():
            return "Welcome!"

    def test_perf_time(self):
        with self.app.test_client() as client:
            response = client.get("/")
            self.assertIsNone(response.headers.get("Perf-Time"))
            response = client.get("/", headers={"perf": "perf-time"})
            perf_time = float(response.headers.get("Perf-Time"))
            self.assertGreater(perf_time, 0.03)
            response = client.get("/", headers={"Perf": "PERF-TIME"})
            self.assertIn("PERF-TIME", response.headers)


class PerfCPUTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        sustainable = Sustainable(self.app)
        sustainable.add_indicator(PerfCPU())

        @self.app.route("/")
        def _():
            return "Welcome!"

    def test_perf_cpu(self):
        with self.app.test_client() as client:
            response = client.get("/")
            self.assertIsNone(response.headers.get("Perf-CPU"))
            response = client.get("/", headers={"perf": "perf-cpu"})
            perf_cpu = float(response.headers.get("Perf-CPU"))
            self.assertGreater(perf_cpu, 0.04)
            response = client.get("/", headers={"Perf": "PERF-CPU"})
            self.assertIn("PERF-CPU", response.headers)


class PerfRAMTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        sustainable = Sustainable(self.app)
        sustainable.add_indicator(PerfRAM())

        @self.app.route("/")
        def _():
            return "Welcome!"

    def test_perf_ram(self):
        with self.app.test_client() as client:
            response = client.get("/")
            self.assertIsNone(response.headers.get("Perf-RAM"))
            response = client.get("/", headers={"perf": "perf-ram"})
            perf_ram = float(response.headers.get("Perf-RAM"))
            self.assertGreater(perf_ram, 0.01)
            response = client.get("/", headers={"Perf": "PERF-RAM"})
            self.assertIn("PERF-RAM", response.headers)


class PerfAllTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        sustainable = Sustainable(self.app)
        sustainable.add_indicator(PerfCPU())
        sustainable.add_indicator(PerfRAM())
        sustainable.add_indicator(PerfTime())

        @self.app.route("/")
        def _():
            return "Welcome!"

    def test_perf_all(self):
        with self.app.test_client() as client:
            response = client.get("/")
            self.assertIsNone(response.headers.get("Perf-CPU"))
            self.assertIsNone(response.headers.get("Perf-RAM"))
            self.assertIsNone(response.headers.get("Perf-Time"))
            response = client.get("/", headers={"perf": "perf-time,perf-cpu,perf-ram"})
            self.assertIn("Perf-CPU", response.headers)
            self.assertIn("Perf-RAM", response.headers)
            self.assertIn("Perf-Time", response.headers)
