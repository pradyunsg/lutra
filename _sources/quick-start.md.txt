# Quick Start

1. Install Lutra from PyPI, in the documentation build environment.

   ```
   pip install lutra
   ```

2. Update `html_theme` in `conf.py`.

   ```py
   html_theme = "lutra"
   ```

3. Build your documentation site with Lutra. ✨

## Is that really it?

For many projects, yes -- if you don't have any errors/warnings in the build, you're good to go.

For other projects, you will need to do more. See {doc}`porting/index` for the details, like how to migrate documentation that uses not-enabled-by-default features from other Sphinx themes.
