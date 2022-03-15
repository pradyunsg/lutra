<!--
 ~ Copyright (c) 2021 Pradyun Gedam
 ~ Licensed under Creative Commons Attribution-ShareAlike 4.0 International License
 ~ SPDX-License-Identifier: CC-BY-SA-4.0
 -->

# Getting Started

Lutra is a theme for Sphinx, a static site generator geared towards technical documentation.

If you're familiar with Python and Sphinx, you can install Lutra with pip, the Python package manager. If you're not, I'd recommend reading the [official Sphinx tutorial][sphinx-tutorial] which provides the necessary background.

[sphinx-tutorial]: https://www.sphinx-doc.org/en/master/tutorial/

## Installation

Lutra is available on the {pypi}`Python Package Index (PyPI) <lutra>` and [GitHub](https://github.com/pradyunsg/lutra), as a Python package.

```console
$ pip install lutra
```

This will install the latest stable release of Lutra, register all the right things for Sphinx to be able to find this theme and install the recommended helpers for documentation authors.

### In-development branch

```console
$ pip install "lutra @ git+https://github.com/pradyunsg/lutra/"
```

This will install the in-development version of Lutra, directly from the GitHub repository. Do this if you want to live on the bleeding edge, with no stability promises. Like the stable installation, Sphinx will be able to find this theme under the same name.

## Using this theme

It is recommended to start with the [Lutra starter template][lutra-template]. To start with that template, you can download it as a zip (under the "code" button) and unzip the code in the same directory as your project.

```{tip}
If you're porting existing Sphinx documentation that uses another theme, you should read: {doc}`../porting/index`.
```

On a Unix system, you can do this by running the following in the root directory of your repository:

```
curl -L https://github.com/pradyunsg/lutra-starter/archive/refs/heads/main.zip -o lutra-starter.zip
unzip lutra-starter.zip
rm lutra-starter.zip
```

This should create the following directory structure:

```
├── .readthedocs.yml
└── docs
    ├── conf.py
    ├── getting-started.md
    ├── index.md
    └── requirements.txt
```

[lutra-template]: https://github.com/pradyunsg/lutra-starter
