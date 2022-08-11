# coding: utf-8

"""This module represents examples of indicator implementation.

For more information about an indicator, see :class:`BaseIndicator`
class.
"""

import time
import tracemalloc

import flask

from flask_sustainable.base import BaseIndicator


class PerfTime(BaseIndicator):
    """Indicator that measure the time of the request.

    When the request is done, the response will contain a header named "Perf-Time"
    with the time of the request in milliseconds.

    Example ::

        from flask_sustainable import Sustainable
        from flask_sustainable.indicator import PerfTime

        app = flask.Flask(__name__)
        sustainable = Sustainable(app)
        sustainable.add_indicator(PerfTime())
    """

    name = "Perf-Time"

    def before_request(self) -> None:
        flask.g.perf_time = time.perf_counter()

    def after_request(self, response: flask.Response) -> flask.Response:
        perf_time = (time.perf_counter() - flask.g.perf_time) * 1000
        response.headers.update({"Perf-Time": f"{perf_time:.5f}"})
        return response


class PerfCPU(BaseIndicator):
    """Indicator that measure the CPU time of the request.

    When the request is done, the response will contain a header named "Perf-CPU"
    with the CPU time of the request in milliseconds.

    The CPU time is the time spent by the process
    that is different from the execution time.

    Example ::

        from flask_sustainable import Sustainable
        from flask_sustainable.indicator import PerfCPU

        app = flask.Flask(__name__)
        sustainable = Sustainable(app)
        sustainable.add_indicator(PerfCPU())
    """

    name = "Perf-CPU"

    def before_request(self) -> None:
        flask.g.perf_cpu = time.process_time()

    def after_request(self, response: flask.Response) -> flask.Response:
        perf_cpu = (time.process_time() - flask.g.perf_cpu) * 1000
        response.headers.update({"Perf-CPU": f"{perf_cpu:.5f}"})
        return response


class PerfRAM(BaseIndicator):
    """Indicator that measure the RAM usage of the request.

    When the request is done, the response will contain a header named "Perf-RAM"
    with the RAM usage of the request in megabytes.

    Example ::

        from flask_sustainable import Sustainable
        from flask_sustainable.indicator import PerfRAM

        app = flask.Flask(__name__)
        sustainable = Sustainable(app)
        sustainable.add_indicator(PerfRAM())
    """

    name = "Perf-RAM"

    def before_request(self) -> None:
        tracemalloc.start()

    def after_request(self, response: flask.Response) -> flask.Response:
        current, _ = tracemalloc.get_traced_memory()
        perf_ram = (current + tracemalloc.get_tracemalloc_memory()) / 10**6
        tracemalloc.stop()
        response.headers.update({"Perf-RAM": f"{perf_ram:.5f}"})
        return response
