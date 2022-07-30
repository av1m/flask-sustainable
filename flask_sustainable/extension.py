# coding: utf-8

import flask

from flask_sustainable.compress import Compression


class Sustainable(object):
    def __init__(self, app=None, **kwargs) -> None:
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        app.after_request(self.after_request)

    def after_request(self, response: flask.Response) -> flask.Response:
        # Compress the response
        response = Compression(response).compress()
        return response
