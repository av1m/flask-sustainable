# Flask-sustainable

[![Python≥3.6](https://img.shields.io/badge/Python-3.6|3.7|3.8|3.9|3.10-blue)](https://docs.python.org/3/whatsnew/3.10.html)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/av1m/flask-sustainable/blob/main/LICENSE)

## Get started 🚀

### Installation 📦

Install the extension with pip:

```bash
pip install flask-sustainable
# Or
pip install git+https://github.com/av1m/flask-sustainable.git
```

### Try it out 🔬

💡 The code is available in [example.py](./example.py) file

```python
import flask
from flask_sustainable import Sustainable
from flask_sustainable.indicator import PerfCPU, PerfRAM, PerfTime

app = flask.Flask(__name__)
sustainable = Sustainable(app)  # Invoke Sustainable().init_app(app)
sustainable.add_indicators(PerfTime(), PerfCPU(), PerfRAM)

@app.route("/")
def helloWorld():
    return "Hello, World!"
```

Then, try with cURL or Postman (or any other HTTP client):

```bash
$ curl http://localhost:5000/ -I -H "Perf: Perf-Time,Perf-CPU Perf-RAM"

Perf-Time: 0.76592
Perf-RAM: 0.12114
Perf-CPU: 0.97900
```

## Developers 👨‍💻

Use python3 or python command (depending on your configuration)
There is a [Makefile](./Makefile) for helping with development.

1. Clone this project

    ```bash
    git clone https://github.com/av1m/flask-sustainable.git
    cd flask-sustainable
    ```

2. Run make command

    ```bash
    make install
    ```

3. Run a sample; a server is running on port 5000

    ```bash
    python example.py
    ```

Everything has been installed and configured correctly! 🎊
Once you modify the code, you can run `make format` and `make test` commands to check the code style and test coverage (through `make coverage`).

To find out all the available commands, you can use `Make Help` :

```bash
help              Display callable targets.
test              Run all tests.
coverage          Run all tests and generate coverage report.
requirements      Install requirements.
install           Install package.
run               Run a example script.
format            Format code.
```

### Tests 🧪

A simple set of tests is included in [tests/](./tests).
To run, simply invoke `make test` or `pytest`.
You can also run a coverage report with `make coverage`.

## Compatibility 🤝

This project is compatible with Python 3.6 and up.
It has been tested on Python 3.6, 3.7, 3.8, 3.9, and 3.10

## License 📃

This project is licensed under the [MIT License](./LICENSE).
