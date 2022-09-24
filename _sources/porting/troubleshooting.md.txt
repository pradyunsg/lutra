(porting-troubleshooting)=

# Troubleshooting issues

Moving between Sphinx themes is a slightly annoying amount of work. This page exists to help you with some of that.

## Get the HTML generation functional

If your `sphinx-build` is succeeding (i.e successfully generating HTML files that you can see), move on to the next section.

### Iterating quicker

### Build _without_ warnings-as-errors

It is fairly common for documentation build scripts to contain `-W`, which makes it a bit more difficult to iterate on your documentation builds quickly.

**Suggestion**: Remove `-W` (temporarily) if you're passing it to the build. This might involve editing the file for the command runner (like Make, Tox, Nox or Just) if you're using one.

### `sphinx-autobuild`

Consider using {pypi}`sphinx-autobuild`. This enables a workflow where saving a file will result in a rebuild and automagically reload the documentation page.

To use it, you need to generate your documentation using `sphinx-autobuild` instead of `sphinx-build` on the command line. An example invocation:

```sh
# Regular command
sphinx-build -b dirhtml docs docs/_build/html
# With automatic reloading on changes to files in docs/
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
