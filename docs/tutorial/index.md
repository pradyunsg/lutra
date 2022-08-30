# Tutorial

...

## Installation

Lutra is available as a Python package on PyPI.

````{tab} Latest
```console
$ pip install lutra
```

This will install the latest stable release of Lutra, register all the right things for Sphinx to be able to find this theme and install the recommended helpers for documentation authors.
````

````{tab} In-development
```console
$ pip install "lutra @ git+https://github.com/pradyunsg/lutra/"
```

This will install the in-development code for Lutra, register all the right things for Sphinx to be able to find this theme and install the recommended helpers for documentation authors.
````

```{hint}
If you're not familiar with Sphinx, I'd recommend reading the [official tutorial][sphinx-tutorial] which provides the necessary background.
```

[sphinx-tutorial]: https://www.sphinx-doc.org/en/master/tutorial/

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
