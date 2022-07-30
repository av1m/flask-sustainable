# coding: utf-8

import copy
import gzip
import logging
import lzma
import zlib

import brotli
import flask
import zstandard

logger = logging.getLogger(__name__)


class Compression(object):
    """Compress the response data when it's possible.

    This class is a wrapper around the flask.Response object.
    It adds the Content-Encoding header to the response.
    The response passed through this class is not modified.

    To do this, it checks the Accept-Encoding header of the request.
    If the client accepts gzip, it compresses the response with gzip.
    If the client accepts br, it compresses the response with br.
    etc.

    Example:
    >>> # Client side
    >>> request.headers["Accept-Encoding"] = "gzip,br,deflate"
    >>> # Server side
    >>> response = flask.Response("Welcome!")
    >>> response = Compression(response).compress()
    >>> response.headers["Content-Encoding"]
    'gzip'
    """

    SUPPORTED_ALGORITHMS: tuple = ("lzma", "zstd", "br", "gzip", "deflate")

    def __init__(self, response: flask.Response) -> None:
        self.accept_encoding = [
            x.lower().strip()
            for x in flask.request.headers.get("Accept-Encoding", "").split(",")
        ]
        logger.debug(self.accept_encoding)
        self.response = copy.deepcopy(response)

    @staticmethod
    def compress_data(algorithm: str, data: bytes, level: int = None) -> bytes:
        """Compress the data with the given algorithm.

        This function raises an KeyError exception if the algorithm is not supported.

        Example:
        >>> data = b"Welcome!"
        >>> Compression.compress_data("gzip", data)
        b'\x1f\x8b\x08\x004\x0c\xe4b\x02\xff\x0bO\xcdI\xce\xcfMU\x04\x00\xd2\xb4B5\x08\x00\x00\x00'

        :param algorithm: The algorithm to use, must be one of the supported algorithms
        :type algorithm: str
        :param data: The data to compress
        :type data: bytes
        :param level: The compression level, if None, the default level is used
        :type level: int
        :return: The compressed data
        :rtype: bytes
        """
        return {
            "gzip": gzip.compress(data, compresslevel=level or 9),
            "br": brotli.compress(data, mode=brotli.MODE_TEXT, quality=level or 0),
            "zstd": zstandard.compress(data, level=level or 22),
            "lzma": lzma.compress(data, preset=level or 9),
            "deflate": zlib.compress(data, level=level or 9),
        }[algorithm]

    def make_response(self, algorithm: str, check: bool = True) -> flask.Response:
        """Make a response with the given algorithm.

        This function change the reponse data and adds the Content-Encoding header.

        Example:
        >>> response = flask.Response("Welcome!")
        >>> response.data
        b'Welcome!'
        >>> response = Compression(response).make_response("gzip")
        >>> response.data
        b'\x1f\x8b\x08\x004\x0c\xe4b\x02\xff\x0bO\xcdI\xce\xcfMU\x04\x00\xd2\xb4B5\x08\x00\x00\x00'
        >>> response.headers["Content-Encoding"]
        'gzip'

        :param algorithm: The algorithm to use, must be one of the supported algorithms
        :type algorithm: str
        :param check: If True, check if the compression is supported (KeyError if not)
        :type check: bool
        :return: The response object
        :rtype: flask.Response
        """
        if check:
            assert algorithm.lower() in self.SUPPORTED_ALGORITHMS
        logger.debug("Compressing with %s", algorithm)
        self.response.content_encoding = algorithm.lower()
        self.response.data = self.compress_data(algorithm.lower(), self.response.data)
        return self.response

    def compress(self, check=False) -> flask.Response:
        """Compress the response data with the highest compression level
        available.

        The order is as follows:
        lzma, zstd, br, gzip, deflate

        Example:
        >>> request.headers["Accept-Encoding"] = "gzip,br,deflate"
        >>> response = flask.Response("Welcome!")
        >>> response = Compression(response).compress()
        >>> response.content_encoding
        'gzip'

        :param check: If True, check if the compression is supported
        :type check: bool
        :return: The response object
        :rtype: flask.Response
        """
        # https://github.com/closeio/Flask-gzip/issues/7
        self.response.direct_passthrough = False
        # Check if the client want any compression
        if "*" in self.accept_encoding:  # Default encoding
            return self.make_response("gzip")

        # Choose the best compression method
        algorithms = ["lzma", "zstd", "br", "gzip", "deflate"]
        for algo in algorithms:
            if algo in self.accept_encoding:
                return self.make_response(algo, check=check)
        return self.response
