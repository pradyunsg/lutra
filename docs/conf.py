# Copyright (c) 2021 Pradyun Gedam
# Licensed under MIT License
# SPDX-License-Identifier: MIT
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""Configuration file for the Sphinx documentation builder.
"""

import os
from typing import Any, Dict

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Lutra"
copyright = "2021 Pradyun Gedam"
author = "Pradyun Gedam"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # Sphinx's own extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    # Our custom extension, only meant for Lutra's own documentation.
    "lutra._sphinxext",
    # External stuff
    "myst_parser",
    "sphinx_inline_tabs",
]

# -- Options for autodoc ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

# Automatically extract typehints when not specified and add them to
# descriptions of the relevant function/methods.
autodoc_typehints = "description"

# Don't show the class signature with the class name.
autodoc_class_signature = "separated"

# -- Options for extlinks ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html#configuration

extlinks = {
    "pypi": ("https://pypi.org/project/%s/", ""),
}

# -- Options for intersphinx -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

# -- Options for TODOs -------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True

# -- Options for Markdown files ----------------------------------------------
# https://myst-parser.readthedocs.io/en/latest/sphinx/reference.html

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
myst_heading_anchors = 3

# -- Options for internationalization ----------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-internationalization

language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "lutra"
html_title = "Lutra"

html_theme_options = {
    # "announcement": (
    #     "This theme is under development and not in a state that it can be used by 'real' projects."
    # ),
    # "announcement_style": "warning",
    # "primary_color": "blue",
    # "accent_color": "violet",
    "hero": {
        "image": "...",
        "primary_text": "...",
        "secondary_text": "...",
    },
    "source_repository": "https://github.com/pradyunsg/lutra/",
    "source_branch": "main",
    "source_directory": "docs/",
    # "navigation_style": "plain",
    # "feedback_form_url": (
    #     "https://docs.google.com/forms/d/e/1FAIpQLSfucp8AnLfSK-2M9kKCMyA5WMYIGPdeMaFa8eHo6ejGFq-nyA/viewform"
    #     "?usp=pp_url&entry.1457058116={page_reference}&entry.702906409={rating}&entry.1161338183={additional_comments}"
    # ),
}

# -- Options for theme development -------------------------------------------
# Make sure all the top-level booleans here are False.

html_css_files = []
html_js_files = []
html_static_path = []
html_context: Dict[str, Any] = {}

DEBUG = False
if DEBUG or "LUTRA_DEBUG" in os.environ:
    html_css_files.append("lutra-debug.css")

RTD_TESTING = False
if RTD_TESTING or "LUTRA_RTD_TESTING" in os.environ:
    html_css_files += [
        "https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css",
        "https://assets.readthedocs.org/static/css/badge_only.css",
    ]
    html_js_files += [
        "readthedocs-dummy.js",
        "https://assets.readthedocs.org/static/javascript/readthedocs-doc-embed.js",
    ]
    html_context["READTHEDOCS"] = True
    html_context["current_version"] = "latest"
    html_static_path += ["_static"]
