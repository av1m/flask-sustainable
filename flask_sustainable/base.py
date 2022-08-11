# coding: utf-8

"""
Base module
===========

This module represent the base class for all indicators and scores.
The contract for each header is indicated in the classes below.
It also explains what indicators and scores are.

It exist two classes that implement theses base class:

- ``indicator`` : correspond to the :file:`indicator.py` module
- ``score`` : correspond to the :file:`score.py` module
"""

from abc import ABCMeta, abstractmethod

import flask


class BaseHeader(metaclass=ABCMeta):
    """Base class for all indicators and scores.

    This class is an abstract class. It must be inherited by all classes
    that are indicators or scores.
    """

    @property
    @abstractmethod
    def name(self):
        """Name of the header.

        The name of the header that the client will ask through "Perf-".
        This name will also be in the response of the request

        The name must be a valid HTTP header name and must not contain any whitespace.
        Plus, it must be unique and don't interfere with other headers.
        Finally, it must start with "Perf-"

        This header will be used in theses scenarios:

        - (server side) In a OPTIONS response to indicate the available headers
        - (client side) In a request through the "Perf" header to indicate
            the headers expected by the client.
        - (server side) In the response to indicate through the name header the value
            of the header.

        :return: Name of the header
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def after_request(self, response: flask.Response) -> flask.Response:
        """Method called after the request.

        This method will be called after each request.
        It can use the :obj:`flask.g` object to get the data stored in the before_request.
        It can also use the response object to modify the response.

        This method is called in the same way as the after_request method of Flask.

        :param response: The initial response object
        :type response: flask.Response
        :return: The response object (modified or not)
        :rtype: flask.Response
        """
        raise NotImplementedError

    def _init_app(self, app: flask.Flask) -> None:
        """Initialize the application.

        This method is only here for development purpose.
        The goal is to test the extension without the need to install it.
        And, without the need of Sustainable class.

        By creating a Flask application, we can use the extension independently.

        .. code-block:: python

            app = flask.Flask(__name__)
            # We assume that the indicator is a subclass of BaseHeader
            indicator = BaseHeader()
            indicator._init_app(app)

        :param app: The flask application
        :type app: flask.Flask
        :return: None
        """
        app.after_request(self.after_request)

    def should_use(self) -> bool:
        """Check if the indicator should be used.

        The indicator/score should be used if the client ask for the header.

        :return: True if the indicator/score should be used, False otherwise
        :rtype: bool
        """
        return (
            self.name.lower() in flask.request.headers.get("Perf", default="").lower()
        )


class BaseIndicator(BaseHeader, metaclass=ABCMeta):
    """Base class for all indicators."""

    @abstractmethod
    def before_request(self) -> None:
        """Method called before the request.

        This method will be called before each request.
        It can be used to do some initialization.

        A good example is to use the flask.g object to store some data.
        This data will be available in the after_request method.

        This method is called in the same way as the :func:`flask.before_request`
        method of Flask.

        :return: None
        """
        raise NotImplementedError

    def _init_app(self, app: flask.Flask) -> None:
        # We call the super class method to initialize the application
        super()._init_app(app)
        # We add the :func:`before_request` method to the application
        app.before_request(self.before_request)


class BaseScore(BaseHeader, metaclass=ABCMeta):
    """Base class for all scores.

    A score is executed after all indicators.

    The name of the score must follow `Perf-ScoreX` where ``X`` is a int > 0.

    The result of a score is called a score.
    A score don't have a :func:`before_request` because his execution comes
    at last.

    Indeed, because all indicators are already used, we can call them to get the score.
    It's possible that a score is not requested by the user, it will not be available
    at the score level.

    It's the responsibility of the implementation to verify whether the indicator
    is present in the headers. If an indicator is required and is not present,
    the function after_request must return none and not raise an exception.
    It would not be appropriate to add a header if the calculation is not possible.

    Example::

        class Example(BaseScore):
            name: str = "Perf-Score1"

            def after_request(self, response):
                indicator = response.headers.get("Perf-Example")
                if not indicator:
                    return
                return indicator ** 2
    """
