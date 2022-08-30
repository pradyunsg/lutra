# On Read the Docs

Lutra is a Sphinx theme and it is fairly common to host Sphinx sites on Read the Docs. They are an open source company, built around Sphinx and its ecosystem. They host the documentation for most open source Python projects.

## Configuration

For building with Lutra on Read the Docs, additional configuration is required to make Lutra available in the documentation build environment. This is done via two files:

- a `docs/requirements.txt` file listing your documentation generation dependencies (like Lutra and any Sphinx extensions you're using).
- a [`.readthedocs.yml`][rtd-config] file pointing Read the Docs to it.

As an example of what that would look like, typically:

```{code-block}
:caption: docs/requirements.txt
:name: rtd-docs-requirements

sphinx
lutra
```

```{code-block}
:caption: .readthedocs.yml
:name: rtd-readthedocs-yml

version: 2

sphinx:
  builder: htmldir
  configuration: docs/conf.py

python:
  version: 3.9
  install:
    - requirements: docs/requirements.txt
    - method: pip
      path: .
```

[rtd-config]: https://docs.readthedocs.io/en/stable/config-file/v2.html
