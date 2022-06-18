# Workflow

This page describes the workflow used during development of this project. It also serves as a reference for the various commands that you would use when working on this project.

## Overview

This project uses the [GitHub Flow] for collaboration.

The codebase contains Python code, [Jinja2]-based HTML pages, [PostCSS] stylesheets and ES6 Javascript code.

- [nox] is used for automating development tasks.
- [pre-commit] is used for running the linters.
- [sphinx-theme-builder] is used to aid theme development and packaging.

## Initial Setup

To work on this project, you need to have git 2.17+ and Python 3.7+. You also need to be on a platform with official releases by the maintainers of NodeJS and Python.

- Clone this project using git:

  ```console
  $ git clone https://github.com/pradyunsg/lutra.git
  $ cd lutra
  ```

- Install `nox`, which provides various commands for the project's development:

  ```console
  $ pip install nox
  ```

You're all set for working on this project.

## Commands

### Code Linting

```console
$ nox -s lint
```

Run the linters, as configured with [pre-commit].

### Local Development Server

```console
$ nox -s docs-live
```

Serve this project's documentation locally, with a development server.

The server watches for changes made to the documentation (`docs/`) or theme(`src/`), which will trigger a rebuild. Once the build is completed, server will automagically reload any open pages using livereload.

```{tip}
My workflow, when I'm working on this theme, is along the lines of:

- Run this command, and wait for the browser window to open.
- <kbd>alt</kbd>+<kbd>tab</kbd> gets me back to my text editor.
- Make changes to some files and save those changes.
- <kbd>alt</kbd>+<kbd>tab</kbd> switches to the browser.
- After a small delay, the change is reflected in the browser.
- If I want to make more changes, <kbd>alt</kbd>+<kbd>tab</kbd> and I'm back to my text editor.
- Repeat the previous 4 steps until happy.

\- @pradyunsg
```

### Documentation Generation

```console
$ nox -s docs
```

Generate the documentation for Lutra into the `build/docs` folder. This generates the same thing as `nox -s docs-live` would serve, but does so by invoking `sphinx-build` directly.

## Release process

- Update the changelog
- Run `nox -s release`
- Once that command succeeds, you're done!

## Installing directly from GitHub

There are times when you might want to install the in-development version of Lutra (mostly for testing that a fix actually does fix things).

```console
$ pip install https://github.com/pradyunsg/lutra.git
```

[github flow]: https://guides.github.com/introduction/flow/
[nox]: https://nox.readthedocs.io/en/stable/
[jinja2]: https://jinja.palletsprojects.com
[sphinx-theme-builder]: https://github.com/pradyunsg/sphinx-theme-builder
[pre-commit]: https://pre-commit.com/
[postcss]: https://postcss.org/
