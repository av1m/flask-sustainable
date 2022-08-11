# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

from pallets_sphinx_themes import ProjectLink

import flask_sustainable

sys.path.insert(0, os.path.abspath("../.."))  # Source code dir relative to this file

project = "Flask-Sustainable"
copyright = "2022, Avi Mimoun"
author = "Avi Mimoun"
version = flask_sustainable.__version__
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

master_doc = "index"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "pallets_sphinx_themes",
]
autoclass_content = "both"
autodoc_typehints = "description"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "werkzeug": ("https://werkzeug.palletsprojects.com/", None),
    "flask": ("https://flask.palletsprojects.com/", None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "flask"
html_static_path = ["_static"]

html_context = {
    "project_links": [
        ProjectLink("PyPI Releases", "https://pypi.org/project/flask-sustainable/"),
        ProjectLink("Source Code", "https://github.com/av1m/flask-sustainable"),
        ProjectLink(
            "Issue Tracker", "https://github.com/av1m/flask-sustainable/issues/"
        ),
        ProjectLink("Documentation", "https://flask-sustainable.readthedocs.io/"),
        ProjectLink("Twitter", "https://twitter.com/avimimoun"),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html", "ethicalads.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html", "ethicalads.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html", "ethicalads.html"]}

html_title = f"{project} Documentation ({version})"
