# coding: utf-8

"""
This module allow to connect a flask application with this package.

We can register this extension to a flask application
and add new indicators and measures to the response.
Also, it add a compression to the response.
"""

import logging

import flask

from flask_sustainable.base import BaseIndicator, BaseMeasure
from flask_sustainable.compress import Compression

logger = logging.getLogger(__name__)


class Sustainable:
    """Flask extension that provide sustainable to a flask application

    This extension add the following features:
    - compress response
    - add new headers about indicators and measures to the response
    """

    def __init__(self, app: flask.Flask = None, **kwargs) -> None:
        self._options = kwargs
        self._registered_indicators: list[BaseIndicator] = []
        self._registered_measures: list[BaseMeasure] = []
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app: flask.Flask, **kwargs) -> None:
        """Initialize the application.

        This method initialize a before and after request method to the application.
        These methods are responsible for adding headers and compression.
        You can check :func:`before_request` and :func:`after_request` methods.

        :param app: The flask application to initialize
        :type app: flask.Flask
        :return: None
        """
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def before_request(self) -> None:
        """When this extension is enabled, this method is called before each request.

        This method don't add any header to the response,
        it only initialize some attributes that will be used
        in the :func:`after_request` method, check :func:`BaseHeader.before_request`

        This method call each :meth:`BaseHeader.before_request` method
        that are registered in the application.
        To register a new BaseHeader, use the :meth:`add_indicator` method.

        Internally, this functions use the :attr:`_registered_indicators` attribute.

        :return: None
        """
        for registered_header in self._registered_indicators:
            if registered_header.should_use():
                registered_header.before_request()

    def after_request(self, response: flask.Response) -> flask.Response:
        """When this extension is enabled, this method is called after each request.

        This method is responsible for the compression and the addition of headers.

        This method call each :meth:`BaseHeader.before_request` method
        that are registered in the application.
        To register a new :class:`BaseHeader`,
        use the :meth:`add_indicator` or :meth:`add_measure` method.

        Internally, this functions use the
        :attr:`_registered_indicators` and :attr:`_registered_measures` attribute
        """
        # Compress the response
        try:
            response = Compression(response).compress(check=True)
        except TypeError as error:
            logger.warning("Error while compressing the response")
            logger.exception(error)
        # Add allowed headers
        if flask.request.method == "OPTIONS":
            headers = [x.name for x in self._registered_indicators]
            response.headers.extend(
                {"Access-Control-Allow-Headers": ", ".join(headers)}
            )
        # Run after_request on all registered headers
        for header in [*self._registered_indicators, *self._registered_measures]:
            if header.should_use():
                header.after_request(response=response)
        return response

    def add_indicator(self, indicator: BaseIndicator) -> None:
        """Add an indicator to the response.

        The rules for the name are available
        in the :func:`indicator.BaseIndicator.name`.

        :param header: Indicator to add, must be a subclass of BaseIndicator
        :type header: BaseIndicator
        :raises AssertionError: If indicator is not a subclass of BaseIndicator
        :return: None
        """
        assert isinstance(
            indicator, BaseIndicator
        ), "Indicator must be a subclass of BaseIndicator"
        assert indicator.name and indicator.name.lower().startswith(
            "perf-"
        ), "Indicator name must start with 'Perf-'"
        self._registered_indicators.append(indicator)

    def add_measure(self, measure: BaseMeasure) -> None:
        """Add a measure to the response.

        The rules for the name are available
        in the :func:`indicator.BaseMeasure.name`.

        :param header: Measure to add, must be a subclass of BaseMeasure
        :type header: BaseMeasure
        :raises AssertionError: If measure is not a subclass of BaseMeasure
        :return: None
        """
        assert isinstance(
            measure, BaseMeasure
        ), "Measure must be a subclass of BaseMeasure"
        # Check if the name is valid
        try:
            assert measure.name.lower().split("perf-score")[1].isnumeric()
        except ValueError as error:
            raise ValueError(
                "Measure name must start with 'Perf-score' and end with a number, "
                "check base.BaseMeasure"
            ) from error
        self._registered_measures.append(measure)
