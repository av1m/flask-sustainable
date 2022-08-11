Flask-sustainable
=================

|Supported Python versions| |License| |Latest Version| |PyPI Publish| |Python CI|

| Flask-Sustainable is an extension for Flask that provides a simple way to add sustainability to your application.
| This is done by compressing the HTTP responses as soon as possible.  
| More, HTTP headers are used so that the server can return information on the performance of the application.

Two types of headers are used:

- indicators
- scores

Get started 🚀
--------------

Installation 📦
~~~~~~~~~~~~~~~~

Install the extension with pip:

.. code:: bash

    pip install flask-sustainable
    # Or
    pip install git+https://github.com/av1m/flask-sustainable.git

Try it out 🔬
~~~~~~~~~~~~~~

💡 The code is available in `example.py <./example.py>`_ file

.. code:: python

    import flask
    from flask_sustainable import Sustainable
    from flask_sustainable.indicator import PerfCPU, PerfRAM, PerfTime

    app = flask.Flask(__name__)
    sustainable = Sustainable(app)  # Invoke Sustainable().init_app(app)
    sustainable.add_indicators(PerfTime(), PerfCPU(), PerfRAM)

    @app.route("/")
    def helloWorld():
        return "Hello, World!"

Then, try with cURL or Postman (or any other HTTP client):

.. code:: bash

    $ curl http://localhost:5000/ -I -H "Perf: Perf-Time,Perf-CPU Perf-RAM"

    Perf-Time: 0.76592
    Perf-RAM: 0.12114
    Perf-CPU: 0.97900

Developers 👨‍💻
----------------

Use python3 or python command (depending on your configuration)
There is a `Makefile <Makefile>`_ for helping with development.

1. Clone this project

.. code:: bash

    git clone https://github.com/av1m/flask-sustainable.git
    cd flask-sustainable

2. Run make command

.. code:: bash

    make install

1. Run a sample; a server is running on port 5000

.. code:: bash
    
    python example.py

Everything has been installed and configured correctly! 🎊
Once you modify the code, you can run `make format` and `make test` commands to check the code style and test coverage (through `make coverage`).

To find out all the available commands, you can use `make help` :

.. code:: bash

    help              Display callable targets.
    test              Run all tests.
    coverage          Run all tests and generate coverage report.
    requirements      Install requirements.
    install           Install package.
    run               Run a example script.
    format            Format code.

Tests 🧪
~~~~~~~~

A simple set of tests is included in `tests/ <./tests>`_.
To run, simply invoke `make test` or `pytest`.
You can also run a coverage report with `make coverage`.

Compatibility 🤝
-----------------

This project is compatible with Python 3.6 and up.
It has been tested on Python 3.6, 3.7, 3.8, 3.9, and 3.10

The Github Actions is not compatible with Python 3.6 because there is no ``setup.py`` file.

License 📃
----------

This project is licensed under the `MIT License <./LICENSE>`_.

.. |Supported Python versions| image:: https://img.shields.io/badge/Python-3.6|3.7|3.8|3.9|3.10-blue
.. |License| image:: http://img.shields.io/:license-MIT-blue.svg
   :target: https://github.com/av1m/flask-sustainable/blob/main/LICENSE
.. |PyPI Publish| image:: https://github.com/av1m/flask-sustainable/actions/workflows/pypi.yml/badge.svg
   :target: https://github.com/av1m/flask-sustainable/actions/workflows/pypi.yml
.. |Python CI| image:: https://github.com/av1m/flask-sustainable/actions/workflows/ci.yaml/badge.svg
   :target: https://github.com/av1m/flask-sustainable/actions/workflows/ci.yaml
.. |Latest Version| image:: https://img.shields.io/pypi/v/Flask-Sustainable.svg
   :target: https://pypi.python.org/pypi/Flask-Sustainable/