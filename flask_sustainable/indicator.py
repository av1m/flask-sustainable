# coding: utf-8

"""This module represents examples of indicator implementation.

For more information about an indicator, see :class:`BaseIndicator`
class.
"""

import time
import tracemalloc

import flask
from codecarbon import OfflineEmissionsTracker

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
        response.headers.update({self.name: f"{perf_time:.5f}"})
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
        response.headers.update({self.name: f"{perf_cpu:.5f}"})
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
        response.headers.update({self.name: f"{perf_ram:.5f}"})
        return response


class PerfEnergy(BaseIndicator):
    """Indicator that measure the energy usage of the request.

    When the request is done, the response will contain a header named
    "Perf-Energy" with the energy usage of the request in watt-seconds.
    """

    name = "Perf-Energy"

    def before_request(self) -> None:
        if not flask.g.get("tracker"):
            flask.g.tracker = OfflineEmissionsTracker(
                country_iso_code="FRA",
                measure_power_secs=3,
                log_level=flask.current_app.logger.level,
                save_to_file=False,
            )
        flask.g.tracker.start()

    def after_request(self, response: flask.Response) -> flask.Response:
        flask.g.tracker.stop()
        # pylint: disable=w0212
        perf_energy_ws = flask.g.tracker._total_energy.kWh * 3.6e6
        response.headers.update({self.name: f"{perf_energy_ws:.5f}"})
        return response


class PerfPower(BaseIndicator):
    """Indicator that measure the power usage of the request.

    When the request is done, the response will contain a header named
    "Perf-Power" with the power usage of the request in watt.
    """

    name = "Perf-Power"

    def before_request(self) -> None:
        if not flask.g.get("tracker"):
            flask.g.tracker = OfflineEmissionsTracker(
                country_iso_code="FRA",
                measure_power_secs=3,
                log_level=flask.current_app.logger.level,
                save_to_file=False,
            )
        flask.g.tracker.start()

    def after_request(self, response: flask.Response) -> flask.Response:
        flask.g.tracker.stop()
        # pylint: disable=w0212
        perf_power = (
            flask.g.tracker._cpu_power.W
            + flask.g.tracker._gpu_power.W
            + flask.g.tracker._ram_power.W
        )
        response.headers.update({self.name: f"{perf_power:.5f}"})
        return response
