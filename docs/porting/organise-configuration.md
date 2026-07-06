# Organise your `conf.py`

This page will walk you through the process of cleaning up and organising a project's `conf.py`, which typically takes about 15 minutes. The goal is to adopt the [improvements from Sphinx >= 5.1's default `conf.py`][conf-py-pr]. Here's [the sort of configuration file you will hopefully end up with][conf-py-example].[^one]

```{admonition} The shortcut
:class: tip
If you don't have a heavily custom `conf.py` file in your project (beyond project name and all), replace it with [the `conf.py` file from the Lutra starter template][starter-conf-py].

Change the `project`, `author`, `extensions` and bring over any extension-specific configuration, and you'll be good to go!
```

[conf-py-pr]: https://github.com/sphinx-doc/sphinx/issues/10056
[conf-py-example]: https://github.com/pradyunsg/installer/blob/main/docs/conf.py
[starter-conf-py]: https://github.com/pradyunsg/lutra-starter/blob/main/docs/conf.py

## Remove comments that are duplicating documentation

Most options have details about how they work available in [Sphinx configuration] documentation. Removing this duplicated content reduces the length of the `conf.py` file significantly and makes the actual assignments more visible.

This is typically the step that takes the most time (expect to spend 5-7 minutes on this).

## Remove unused configuration

If you don't publish your documentation as an ePub or man pages, remove the configuration for those things. Do the same for any extensions that you don't use.

## Group _everything_ into sections

Chances are, if you've added configuration keys or custom functions, the file has contents scattered all around. Move them and group them, with the separator serving as a marker to split the individual groups.

- Use the same headings as [Sphinx configuration] documentation for the section names, for grouping of the built-in Sphinx configuration options.
- Use the extension name as the section name, for extension-specific options.

If you've done this right, you'll now have an "Options for HTML output" section, which has your HTML-related configuration and most of the theme-specific configuration as well. This is useful -- when changing your theme to Lutra, you will only change things in this section (hopefully[^broken-dreams]).

## Add the documentation URL to the each section

This makes it easier to get to the relevant documentation pages, since you can copy-paste or, on most GUI editors, ctrl+click or cmd+click on these links to get to the detailed complete documentation.

## Remove same-as-default configuration values (optional-ish)

This makes it clearer what non-default behaviours the documentation depends on. Basically, the thought process here is: fewer configuration options set -> less complex `conf.py` -> easier to understand and maintain.

[sphinx configuration]: https://www.sphinx-doc.org/en/master/usage/configuration.html

[^broken-dreams]: To put it bluntly, there are going to be documentation sets that do all kinds of stuff in the `conf.py` file. When it's got that, it'll probably need changes in many places.

[^one]: This is the style used by Sphinx's default generation, starting Sphinx 5.1.
