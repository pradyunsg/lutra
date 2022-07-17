# Porting to Lutra

Welcome! Happy to see that you're trying this theme! :)

This document serves as a walk-through, to help you port your existing Sphinx documentation over to Lutra.

```{toctree}
:hidden:
:glob:

organise-configuration
troubleshooting
theme-*
```

## Clean up your `conf.py` file (optional)

I'd highly recommend going through the following guide: {doc}`organise-configuration`. It'll make future maintenance (and the porting process) easier.

## Start using Lutra

1. Install Lutra from PyPI.

   ```
   pip install lutra
   ```

2. After ensuring you have Lutra installed in the documentation build environment, update your `html_theme` in `conf.py` to point to Lutra:

   ```py
   html_theme = "lutra"
   ```

   For most projects, that's all you need to do -- specifically, if your documentation has no existing `html_theme_options`, no custom templates and no "special" extensions.

3. Build your documentation site. If that didn't succeed, see {doc}`./troubleshooting`.

4. Open up your documentation site, and look around. If you spot anything that's broken, see {ref}`porting-faq`.

## Configure Read the Docs

```{hint}
This is only relevant if you're using Read the Docs for hosting your project documentation.
```

For building with Lutra on Read the Docs, you need to tell Read the Docs to make the theme available in the build environment. Their build system automatically make `sphinx-rtd-theme` (and default Sphinx themes) available but all other themes need additional configuration in their build environment.

To do this, you need to have two files:

- a `docs/requirements.txt` file listing your documentation generation dependencies.
- a [`.readthedocs.yml`][rtd-config] file configuring Read the Docs to generate the documentation correctly.

As an example of what that would look like, minimally:

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
