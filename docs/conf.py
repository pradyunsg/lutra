"""Configuration file for the Sphinx documentation builder."""

import os
from typing import Any, Dict

# from lutra import create_linkcode_resolve

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Lutra (WIP)"
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
    # "sphinx.ext.linkcode",
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
    "pypi": ("https://pypi.org/project/%s/", "%s"),
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
lutra_hero = {
    "brand": "Lutra",
    "tagline": (
        "A work in progress Sphinx theme."
        # "Clean, modern, and powerful.<br>Meet the Sphinx theme you've always wanted."
    ),
    "features": [
        {
            "title": "Designed for the modern web",
            "details": (
                """
                Lutra is responsive, lightweight, and utilises modern web browser
                features while degrading gracefully. Build documentation websites
                that work on all devices.
                """
            ),
        },
        {
            "title": "Deeply customizable",
            "details": (
                """
                From unparalleled flexibility in navigation and layouts, to tweaking
                colors and fonts, and so much more. Create beautiful documentation that
                matches your brand and vision.
                """
            ),
        },
        {
            "title": "All the good stuff from Sphinx",
            "details": (
                """
                With built-in support for everything you can do with standard Sphinx as
                well as a curated selection of extensions, you have everything you need
                to create awesome documentation.
                """
            ),
        },
        {
            "title": "Built for everyone",
            "details": (
                """
                With a focus on accessibility [WIP: and internationalization, including
                full RTL (right-to-left) support,] Lutra helps make your documentation
                work for everyone.
                """
            ),
        },
        {
            "title": "Scales with your project",
            "details": (
                """
                From single-page websites to sprawling, complex, and extensive websites,
                Lutra can gracefully adapt to your documentation needs.
                """
            ),
        },
        {
            "title": "Powerful yet easy to use",
            "details": (
                """
                The large set of [WIP: well-documented] features make it possible to
                create documentation that works the way you want it to. A zero
                configuration foundation makes it easy to get started.
                """
            ),
        },
    ],
    "actions": [
        {
            "style": "brand",
            "text": "Get Started →",
            "doc": "get-started",
        },
        {
            "style": "alt",
            "text": "View on GitHub",
            "href": "https://github.com/pradyunsg/lutra/",
        },
    ],
}

html_additional_pages = {
    "index": "hero.html",
}

html_theme_options = {
    # "announcement": (
    #     "This theme is under development and not in a state that it can be "
    #     "used by 'real' projects."
    # ),
    # "announcement_style": "warning",
    # "primary_color": "blue",
    # "secondary_color": "violet",
    "source_repository": "https://github.com/pradyunsg/lutra/",
    "source_branch": "main",
    "source_directory": "docs/",
    "navigation_style": "tabs-document",
    "hero": lutra_hero,
    # Below are TODOs.
    # "feedback_form_url": (
    #     "https://docs.google.com/forms/d/e/1FAIpQLSfucp8AnLfSK-2M9kKCMyA5WMYIGPdeMaFa8eHo6ejGFq-nyA/viewform"
    #     "?usp=pp_url&entry.1457058116={page_reference}&entry.702906409={rating}
    #      &entry.1161338183={additional_comments}"
    # ),
}

# -- Options for linkcode -------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html#configuration

# linkcode_resolve = lutra.create_linkcode_resolve(
#     project=project,
#     html_theme_options=html_theme_options,
# )

# -- Options for theme development -------------------------------------------
# Make sure all the top-level booleans here are False.

html_css_files = []
html_js_files = []
html_static_path = []
html_context: Dict[str, Any] = {
    # "current_version": 0,
    # "versions": [
    #     ("dev (3.12)", "/en/3.12/"),
    #     ("pre (3.11)", "/en/3.11/"),
    #     ("3.10", "/en/3.10/"),
    # ],
    # "current_language": 0,
    # "languages": [
    #     ("English", "/en/3.12/"),
    #     ("Hindi", "/hindi/3.12/"),
    # ],
}

DEBUG = False
if DEBUG or "styles" in os.environ.get("LUTRA_DEBUG", ""):
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
