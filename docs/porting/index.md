<!--
 ~ Copyright (c) 2021 Pradyun Gedam
 ~ Licensed under Creative Commons Attribution-ShareAlike 4.0 International License
 ~ SPDX-License-Identifier: CC-BY-SA-4.0
 -->

# Porting to Lutra

Welcome! Happy to see that you liked this theme enough to try using it! :)

This document serves as a guide for porting existing Sphinx documentation to use Lutra. Notably, it contains troubleshooting advice, to help you identify issues.

```{toctree}
alabaster
sphinx-rtd-theme
pydata-sphinx-theme
sphinx-book-theme
furo
```

## Start using Lutra

You can install Lutra from PyPI.

```
pip install lutra
```

Update your `html_theme` in `conf.py`, to use Lutra:

```py
html_theme = "lutra"
```

If your documentation is straightforward, not on the happy path, If that didn't "just work", , see the {ref}`organise-build-configuration` and {ref}`porting-troubleshooting` sections below.

## Configure Read the Docs

If you're using Read the Docs for hosting your documentation, you might want to ensure that your repository has:

- a `docs/requirements.txt` file listing your documentation generation dependencies.
- a [`.readthedocs.yml`][rtd-config] file configuring Read the Docs to generate the documentation correctly.

For example:

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

(organise-build-configuration)=

## Organise your `conf.py`

The default `conf.py` file that Sphinx generates (through `sphinx-quickstart`) is basically unmaintainable, [in my opinion](https://github.com/sphinx-doc/sphinx/issues/10056). Chances are, you've never really bothered to clean it up. You should! Doing this is going to extremely valuable, by making it very easy for you to identify things that might be problematic and make it easier to understand as well.

If you don't care too strongly about the existing contents of your conf.py (beyond project name and such), replace it with [the `conf.py` file from the Lutra starter template][starter-conf-py] instead.

Here's a step-by-step guide for improving your `conf.py` to be more maintainable (like [this configuration file][conf-py-example]):

1. **Remove comments that are duplicating information**

   Most options have details about how they work available in [Sphinx configuration] documentation. Removing this duplicated content reduces the length of the `conf.py` file significantly and makes the actual assignments more visible.

2. **Group configuration options into sections**

   - Use the same headings as [Sphinx configuration] documentation for the section names.
   - Use the extension name as the section name, for extension-specific options.

3. **Remove unused sections**

   If you don't publish your documentation as an ePub or man pages, remove the configuration for those things. Do the same for any extensions that you don't use anymore.

4. **Add the documentation URL to the each section**

   This makes it easier to get to the relevant documentation pages, since you can copy-paste or, on most GUI editors, ctrl+click or cmd+click on these links to get to the detailed complete documentation.

5. **Remove same-as-default configuration values** (optional-ish).

   This makes it clearer what non-default behaviours the documentation depends on. Plus, fewer configuration options set -> less complex `conf.py` -> easier to understand and maintain.

If you've done this right, you'll now have an "Options for HTML output" section, which has your HTML-related configuration and most of the theme-specific configuration as well.

(porting-troubleshooting)=

## Troubleshooting

If things are not working for some reason, either the documentation build is failing or your page's markup looks completely wrong, you'll need to debug the configuration file and/or the documentation sources. This section aims to provide guidance to make things easier.

### Build without warnings-as-errors

It is fairly common for documentation build scripts to contain `-W`, which makes it a bit more difficult to iterate on your documentation builds quickly.

### `sphinx-autobuild`

You should consider using {pypi}`sphinx-autobuild`. This enables a workflow where saving a file will result in a rebuild and automagically reload the documentation page.

To use it, you need to generate your documentation using `sphinx-autobuild` instead of `sphinx-build` on the command line. An example invocation:

```
sphinx-autobuild -b dirhtml docs docs/_build/html
```

This is _very_ useful for iterating through changes to your documentation quickly.

### Check for interfering configuration options

There's quite a few configuration options that can interfere with how your documentation looks with Lutra. It's a good idea to remove these for the initial port -- you might not need to re-enable these options!

Here's a non-exhaustive list, of [Sphinx configuration] options that are known to interfere with the output of the theme:

- `pygments_style`
- `html_context`
- `html_style`
- `html_static_path`
- `html_css_files`
- `html_js_files`
- `html_theme_options`
- `html_sidebars`
- `html_additional_pages`
- `html4_writer`

### Disable extensions

Most Sphinx extensions are well-behaved and do not interfere with the theme being used. However, there are certainly some "enterprising" extensions that do extremely invasive things, while also making bad assumptions that can result in broken behaviours.

To accomodate for this, try disabling any extensions that do not follow the `sphinx.ext.*` naming style.

[conf-py-example]: https://github.com/pradyunsg/installer/blob/main/docs/conf.py
[sphinx configuration]: https://www.sphinx-doc.org/en/master/usage/configuration.html
[rtd-config]: https://docs.readthedocs.io/en/stable/config-file/v2.html
[starter-conf-py]: https://github.com/pradyunsg/lutra-starter/blob/main/docs/conf.py
