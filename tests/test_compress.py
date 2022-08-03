"""Class test for compress.py module."""

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import gzip
import lzma
import sys
import unittest
import zlib

import brotli
import zstandard
from flask import Flask, Response

from flask_sustainable.compress import Compression
from flask_sustainable.extension import Sustainable


class CompressTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        Sustainable(self.app)

        @self.app.route("/")
        def _():
            return "Welcome!"

    def test_gzip(self):
        with self.app.test_client() as client:
            response = client.get("/", headers={"Accept-Encoding": "gzip"})
            self.assertEqual(response.headers["Content-Encoding"], "gzip")
            # Decompress gzip
            welcome = gzip.decompress(response.data)
            self.assertEqual(welcome, b"Welcome!")

    def test_brotli(self):
        with self.app.test_client() as client:
            response = client.get("/", headers={"Accept-Encoding": "br"})
            print(response.headers["Content-Encoding"])
            self.assertEqual(response.headers["Content-Encoding"], "br")
            # Decompress brotli
            welcome = brotli.decompress(response.data)
            self.assertEqual(welcome, b"Welcome!")

    def test_zstd(self):
        with self.app.test_client() as client:
            response = client.get("/", headers={"Accept-Encoding": "zstd"})
            self.assertEqual(response.headers["Content-Encoding"], "zstd")
            # Decompress zstd
            welcome = zstandard.decompress(response.data)
            self.assertEqual(welcome, b"Welcome!")

    def test_lzma(self):
        with self.app.test_client() as client:
            response = client.get("/", headers={"Accept-Encoding": "lzma"})
            self.assertEqual(response.headers["Content-Encoding"], "lzma")
            # Decompress lzma
            welcome = lzma.decompress(response.data)
            self.assertEqual(welcome, b"Welcome!")

    def test_deflate(self):
        with self.app.test_client() as client:
            response = client.get("/", headers={"Accept-Encoding": "deflate"})
            self.assertEqual(response.headers["Content-Encoding"], "deflate")
            # Decompress deflate
            welcome = zlib.decompress(response.data)
            self.assertEqual(welcome, b"Welcome!")

    def test_unknow(self):
        with self.app.test_client() as client:
            response = client.get("/", headers={"Accept-Encoding": "unknow"})
            self.assertNotIn("Content-Encoding", response.headers)
            self.assertEqual(response.data, b"Welcome!")

    def test_all(self):
        algorithm = Compression.SUPPORTED_ALGORITHMS[0]
        with self.app.test_client() as client:
            response = client.get("/", headers={"Accept-Encoding": "*"})
            # By default, will use gzip
            self.assertEqual(response.headers["Content-Encoding"], algorithm)
            self.assertEqual(response.content_encoding, algorithm)
            # Decompress gzip
            welcome = sys.modules[algorithm].decompress(response.data)
            self.assertEqual(welcome, b"Welcome!")


class CompressDataTestCase(unittest.TestCase):
    def setUp(self):
        self.message = b"Welcome!"
        self.decompress = {
            "lzma": lzma.decompress,
            "zstd": zstandard.decompress,
            "br": brotli.decompress,
            "gzip": gzip.decompress,
            "deflate": zlib.decompress,
        }

    def test_simple(self):
        for name, func in self.decompress.items():
            with self.subTest(name=name):
                encoded = Compression.compress_data(name, self.message)
                data = func(encoded)
                self.assertEqual(data, self.message)

    def test_level(self):
        for name, func in self.decompress.items():
            with self.subTest(name=name):
                encoded = Compression.compress_data(name, self.message, level=9)
                data = func(encoded)
                self.assertEqual(data, self.message)


class ResponseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.response: Response = self.app.make_response("Welcome!")
        self.decompress = {
            "lzma": lzma.decompress,
            "zstd": zstandard.decompress,
            "br": brotli.decompress,
            "gzip": gzip.decompress,
            "deflate": zlib.decompress,
        }

    def test_all(self) -> None:
        with self.app.test_request_context():
            for name, func in self.decompress.items():
                with self.subTest(name=name):
                    # Test also the immutability of "response"
                    response = Compression(self.response).make_response(name)
                    data = func(response.data)
                    self.assertEqual(data, b"Welcome!")


class AcceptEncodingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)

        @self.app.route("/")
        def _():
            return "Welcome!"

    def test_parse(self):
        with self.app.test_client() as client:
            client.get("/", headers={"Accept-Encoding": "gzip, deflate"})
